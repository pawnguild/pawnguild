from pawnlisting.models import Pawn
from django.shortcuts import reverse

from pawnlisting.tests.utility import UtilityTestCase

class LoginRequiredTests(UtilityTestCase):

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_pawn_add_redirects_anonymous(self):
        response = self.client.get(reverse("create_pawn"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('create_pawn')}")

    def test_update_pawn_redirects_anonymous(self):
        pawn_update_url = reverse("update_pawn", kwargs={"pk": self.pawn.id})
        response = self.client.get(pawn_update_url)
        self.assertRedirects(response, f"{reverse('login')}?next={pawn_update_url}")

    def test_pawn_delete_redirects_anonymous(self):
        pawn_delete_url = reverse("delete_pawn", kwargs={"pk": self.pawn.id})
        response = self.client.get(pawn_delete_url)
        self.assertRedirects(response, f"{reverse('login')}?next={pawn_delete_url}")
    

class PawnCreateTests(UtilityTestCase):

    def test_pawn_add_no_redirect_logged_in(self):
        self.register_user_log_in("TestUser")
        response = self.client.get(reverse("create_pawn"))
        self.assertEqual(response.status_code, 200)

    def test_can_create_pawn_when_logged_in(self):
        self.register_user_log_in("TestUser")
        pawn_data, profile_data = self.generate_pawn_data(name="yoshi", platform="Steam")

        post_data = {**pawn_data, **profile_data}
        response = self.client.post(reverse("create_pawn"), post_data)
        self.assertEqual(response.status_code, 302)

        created_pawn = Pawn.objects.get(**pawn_data)
        self.assertTrue(created_pawn) # If this fails, pawn doesn't exist, which means pawn creation does not work
        self.assertEqual(created_pawn.created_by, self.user)

        created_profile = created_pawn.steampawnprofile
        self.assertEqual(created_profile.steam_url, "https://steamcommunity.com/id/Yellow_Yoshi/")


class PawnDetailTests(UtilityTestCase):

    def test_detail_view(self):
        response = self.client.get(reverse("view_pawn", kwargs={"pk": self.pawn.id}))
        self.assertEqual(response.status_code, 200)


class PawnUpdateTests(UtilityTestCase):

    def test_403_logged_in_not_owner(self):
        self.register_user_log_in(username="TestUser2")
        pawn_id = self.pawn.id
        response = self.client.get(reverse("update_pawn", kwargs={"pk": pawn_id}))
        self.assertEqual(response.status_code, 403)

    def test_update_pawn(self):
        self.register_user_log_in("TestUser")
        pawn_data, pawn_profile_data = self.generate_pawn_data(name="TestPawn", platform="Switch", level=72)
        response = self.client.post(reverse("update_pawn", kwargs={"pk": self.pawn.id}), pawn_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("view_pawn", kwargs={"pk": self.pawn.id}))
        self.assertTrue(Pawn.objects.get(**pawn_data))


class DeletePawnTests(UtilityTestCase):

    def setUp(self):
        super().setUp()
        self.pawn2, self.pawn2_profile = self.createPawnAndProfile(self.user, "Pawn2", "Switch")

    def test_403_logged_in_not_owner(self):
        self.register_user_log_in("TestUser2")
        response = self.client.post(reverse("delete_pawn", kwargs={"pk": self.pawn2.id}))
        self.assertEqual(response.status_code, 403)

    def test_delete_pawn(self):
        self.register_user_log_in("TestUser")
        response = self.client.post(reverse("delete_pawn", kwargs={"pk": self.pawn2.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("manage_pawns"))