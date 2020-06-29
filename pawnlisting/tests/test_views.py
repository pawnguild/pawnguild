from django.test import TestCase, Client
from pawnlisting.models import Pawn
from django.contrib.auth import get_user_model
from django.shortcuts import reverse


from crum import get_current_user, impersonate

class Utility:

    def setUp(self):
        self.client = Client()

    def generate_pawn_data(self, name, level=50, vocation="Mage", gender="Male", primary_inclination="Nexus", secondary_inclination="Pioneer"):
        return {"name": name, "level": level, "vocation": vocation, "gender": gender,
            "primary_inclination": primary_inclination, "secondary_inclination": secondary_inclination}

    def create_user_log_in(self, username):
        user, created = get_user_model().objects.get_or_create(username=username)
        user.set_password("12345")
        user.save()
    
        self.client.login(username=username, password="12345")
        return user

class PawnCreateTests(Utility, TestCase):

    def test_pawn_add_redirects_not_logged_in(self):
        response = self.client.get(reverse("create_pawn"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('create_pawn')}")

    def test_cannot_create_pawn_when_not_logged_in(self):
        response = self.client.post(reverse("create_pawn"), self.generate_pawn_data("T1"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('create_pawn')}")

    def test_pawn_add_no_redirect_logged_in(self):
        self.create_user_log_in("T1")
        response = self.client.get(reverse("create_pawn"))
        self.assertEqual(response.status_code, 200)

    def test_can_create_pawn_when_logged_in(self):
        self.create_user_log_in("T2")
        pawn_data = self.generate_pawn_data(name="yoshi")
        response = self.client.post(reverse("create_pawn"), pawn_data)
        self.assertRedirects(response, "/list/")
        pawn = Pawn.objects.get(**pawn_data)
        self.assertTrue(pawn) # If this fails, pawn doesn't exist, which means pawn creation does not work


class UpdatePawnTests(Utility, TestCase):

    def setUp(self):
        Utility.__init__(self)
        user = self.create_user_log_in("T3")
        pawn_data = self.generate_pawn_data(name="T3_pawn")
        with impersonate(user):
            pawn = Pawn.objects.create(**pawn_data)

        self.created_pawn = pawn

    def test_login_redirect_not_logged_in(self):
        self.client.logout()
        pawn_id = self.created_pawn.id
        pawn_update_url = reverse("update_pawn", kwargs={"pk": pawn_id})
        response = self.client.get(pawn_update_url)
        self.assertRedirects(response, f"{reverse('login')}?next={pawn_update_url}")

    def test_403_logged_in_not_owner(self):
        self.create_user_log_in(username="T2")
        pawn_id = self.created_pawn.id
        response = self.client.get(reverse("update_pawn", kwargs={"pk": pawn_id}))
        self.assertEqual(response.status_code, 403)

    def test_update_pawn(self):
        self.create_user_log_in("T3")
        pawn_id = self.created_pawn.id
        response = self.client.post(reverse("update_pawn", kwargs={"pk": pawn_id}), data=self.generate_pawn_data(name="new_pawn_name"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("list_pawn"))