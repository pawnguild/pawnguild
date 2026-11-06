from datetime import timedelta
import re
from unittest.mock import patch
from urllib.parse import urlsplit

from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.contrib.auth.tokens import default_token_generator
from django.core import mail, signing
from django.shortcuts import reverse
from django.test import Client, TestCase, override_settings

from django_email_verification import send_email


class PasswordRecoveryTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="recovery-user",
            email="recovery@example.com",
            password="original-good-password-852",
        )

    def request_reset(self, identifier):
        return self.client.post(
            reverse("password_reset_recover"),
            {"username_or_email": identifier},
            secure=True,
        )

    def reset_link(self):
        self.request_reset(self.user.username)
        return urlsplit(re.search(r"https://\S+", mail.outbox[-1].body)[0]).path

    def test_username_and_email_recovery_send_working_links(self):
        for identifier in (self.user.username, self.user.email.upper()):
            with self.subTest(identifier=identifier):
                before = len(mail.outbox)
                response = self.request_reset(identifier)
                self.assertRedirects(response, reverse("password_reset_sent"))
                self.assertEqual(len(mail.outbox), before + 1)
                self.assertEqual(mail.outbox[-1].to, [self.user.email])
                link = urlsplit(re.search(r"https://\S+", mail.outbox[-1].body)[0]).path
                response = self.client.get(link, follow=True, secure=True)
                self.assertTrue(response.context["validlink"])
                self.assertContains(response, 'name="new_password1"')

    def test_password_can_be_reset_once_and_new_credentials_work(self):
        link = self.reset_link()
        response = self.client.get(link, follow=True, secure=True)
        form_url = response.redirect_chain[-1][0]
        response = self.client.post(
            form_url,
            {
                "new_password1": "replacement-good-password-974",
                "new_password2": "replacement-good-password-974",
            },
            secure=True,
        )
        self.assertRedirects(response, "/reset/done/")
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("replacement-good-password-974"))
        response = self.client.get(link, follow=True, secure=True)
        self.assertFalse(response.context["validlink"])
        self.assertTrue(
            self.client.login(
                username=self.user.email, password="replacement-good-password-974"
            )
        )

    def test_weak_reset_password_is_rejected_without_changing_password(self):
        response = self.client.get(self.reset_link(), follow=True, secure=True)
        form_url = response.redirect_chain[-1][0]
        response = self.client.post(
            form_url,
            {"new_password1": "123", "new_password2": "123"},
            secure=True,
        )
        self.assertIn("new_password2", response.context["form"].errors)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("original-good-password-852"))

    def test_unknown_and_inactive_accounts_do_not_receive_reset_email(self):
        self.user.is_active = False
        self.user.save()
        for identifier in ("nonexistent", self.user.email):
            response = self.request_reset(identifier)
            self.assertRedirects(response, reverse("password_reset_sent"))
        self.assertEqual(len(mail.outbox), 0)

    def test_expired_and_forged_reset_links_are_rejected(self):
        link = self.reset_link()
        future = default_token_generator._now() + timedelta(days=3)
        with patch.object(default_token_generator, "_now", return_value=future):
            response = self.client.get(link, follow=True, secure=True)
        self.assertFalse(response.context["validlink"])
        response = self.client.get(link.rstrip("/") + "forged/", secure=True)
        self.assertContains(response, "password reset link is invalid")

    def test_old_reset_links_offer_a_fresh_request_without_changing_account(self):
        token = signing.dumps(self.user.pk, salt="password_recovery")
        response = self.client.get("/reset/" + token + "/", secure=True)
        self.assertContains(response, "password reset link is invalid")
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("original-good-password-852"))

    def test_standard_reset_routes_keep_the_sites_templates(self):
        response = self.client.get("/password_reset/")
        self.assertContains(response, 'name="username_or_email"')
        response = self.client.get("/password_reset/done/")
        self.assertContains(response, "If an active account matches")


class AccountUpgradeTests(TestCase):
    @override_settings(
        PASSWORD_HASHERS=["django.contrib.auth.hashers.PBKDF2PasswordHasher"]
    )
    def test_django_32_password_hash_still_authenticates(self):
        password = PBKDF2PasswordHasher().encode(
            "legacy-good-password-491", "synthetic-legacy-salt", iterations=320000
        )
        user = get_user_model().objects.create(
            username="legacy-user", email="legacy@example.com", password=password
        )
        self.assertTrue(
            self.client.login(
                username=user.username, password="legacy-good-password-491"
            )
        )
        self.assertTrue(get_user(self.client).is_authenticated)

    def test_logout_requires_csrf_protected_post(self):
        user = get_user_model().objects.create_user(username="logout-user")
        client = Client(enforce_csrf_checks=True)
        client.force_login(user)
        self.assertEqual(client.get(reverse("logout")).status_code, 405)
        self.assertEqual(client.post(reverse("logout")).status_code, 403)
        client.get(reverse("home"))
        token = client.cookies["csrftoken"].value
        response = client.post(reverse("logout"), {"csrfmiddlewaretoken": token})
        self.assertRedirects(response, "/")
        self.assertFalse(get_user(client).is_authenticated)

    def test_registration_and_existing_email_verification_format_work(self):
        # Send synchronously into the in-memory email backend; never use SMTP.
        with patch(
            "pawnguild.registration.views.send_email",
            side_effect=lambda user: send_email(user, thread=False),
        ):
            response = self.client.post(
                reverse("register"),
                {
                    "username": "verification-user",
                    "email": "verification@example.com",
                    "password1": "registration-good-password-472",
                    "password2": "registration-good-password-472",
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(get_user(self.client).is_authenticated)
        link = re.search(r"pawnguild.xyz(/email/[^\s]+)", mail.outbox[0].body)[1]
        response = self.client.get(link)
        self.assertContains(response, "You have confirmed your account")
        user = get_user_model().objects.get(username="verification-user")
        self.assertTrue(user.email_verified)
        forged = link[:-1] + ("0" if link[-1] != "0" else "1")
        response = self.client.get(forged)
        self.assertContains(response, "Invalid token")
