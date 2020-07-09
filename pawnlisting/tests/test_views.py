from django.test import TestCase, Client
from pawnlisting.models import Pawn
from django.shortcuts import reverse


from crum import get_current_user, impersonate

from pawnlisting.tests.utility import Utility

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
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Pawn.objects.get(**pawn_data)) # If this fails, pawn doesn't exist, which means pawn creation does not work


class PawnDetailTests(Utility, TestCase):
     
    def setUp(self):
         user = self.create_user_log_in("T1")
         with impersonate(user):
             self.created_pawn = Pawn.objects.create(**self.generate_pawn_data("pawn_T1"))

    def test_detail_view(self):
        response = self.client.get(reverse("view_pawn", kwargs={"pk": self.created_pawn.id}))
        self.assertEqual(response.status_code, 200)


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
        pawn_data = self.generate_pawn_data(name="new_pawn_name")
        response = self.client.post(reverse("update_pawn", kwargs={"pk": self.created_pawn.id}), pawn_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("view_pawn", kwargs={"pk": self.created_pawn.id}))
        self.assertTrue(Pawn.objects.get(**pawn_data))


class DeletePawnTests(Utility, TestCase):

    def setUp(self):
        Utility.__init__(self)
        user = self.create_user_log_in("T1")
        
        with impersonate(user):
            pawn = Pawn.objects.create(**self.generate_pawn_data("pawn_T1"))
        
        self.created_pawn = pawn

    def test_login_redirect_not_logged_in(self):
        self.client.logout()
        pawn_id = self.created_pawn.id
        pawn_delete_url = reverse("delete_pawn", kwargs={"pk": pawn_id})
        response = self.client.get(pawn_delete_url)
        self.assertRedirects(response, f"{reverse('login')}?next={pawn_delete_url}")
    
    def test_403_logged_in_not_owner(self):
        self.create_user_log_in("T2")
        response = self.client.post(reverse("delete_pawn", kwargs={"pk": self.created_pawn.id}))
        self.assertEqual(response.status_code, 403)

    def test_delete_pawn(self):
        self.create_user_log_in("T1")
        response = self.client.post(reverse("delete_pawn", kwargs={"pk": self.created_pawn.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("list_pawn"))