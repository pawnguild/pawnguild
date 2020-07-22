from pawnlisting.models import SteamPawn, SwitchPawn, XboxOnePawn
from django.shortcuts import reverse

from pawnlisting.tests.utility import UtilityTestCase

class LoginRequiredTests(UtilityTestCase):

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_pawn_add_redirects_anonymous(self):
        response = self.client.get(reverse("select_platform"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('select_platform')}")

        response = self.client.get(reverse("create-steam-pawn"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('create-steam-pawn')}")

        response = self.client.get(reverse("create-switch-pawn"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('create-switch-pawn')}")

        response = self.client.get(reverse("create-xbox1-pawn"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('create-xbox1-pawn')}")

    def test_update_pawn_redirects_anonymous(self):
        steam_pawn_update_url = reverse("update-steam-pawn", kwargs={"pk": self.steam_pawn.id})
        response = self.client.get(steam_pawn_update_url)
        self.assertRedirects(response, f"{reverse('login')}?next={steam_pawn_update_url}")

        switch_pawn_update_url = reverse("update-switch-pawn", kwargs={"pk": self.switch_pawn.id})
        response = self.client.get(switch_pawn_update_url)
        self.assertRedirects(response, f"{reverse('login')}?next={switch_pawn_update_url}")

        xbox1_pawn_update_url = reverse("update-xbox1-pawn", kwargs={"pk": self.xbox1_pawn.id})
        response = self.client.get(xbox1_pawn_update_url)
        self.assertRedirects(response, f"{reverse('login')}?next={xbox1_pawn_update_url}")

    def test_pawn_delete_redirects_anonymous(self):
        steam_pawn_delete_url = reverse("delete-steam-pawn", kwargs={"pk": self.steam_pawn.id})
        response = self.client.get(steam_pawn_delete_url)
        self.assertRedirects(response, f"{reverse('login')}?next={steam_pawn_delete_url}")
    
        switch_pawn_delete_url = reverse("delete-switch-pawn", kwargs={"pk": self.switch_pawn.id})
        response = self.client.get(switch_pawn_delete_url)
        self.assertRedirects(response, f"{reverse('login')}?next={switch_pawn_delete_url}")

        xbox1_pawn_delete_url = reverse("delete-xbox1-pawn", kwargs={"pk": self.xbox1_pawn.id})
        response = self.client.get(xbox1_pawn_delete_url)
        self.assertRedirects(response, f"{reverse('login')}?next={xbox1_pawn_delete_url}")


class PawnCreateTests(UtilityTestCase):

    def test_pawn_add_no_redirect_logged_in(self):
        response = self.client.get(reverse("select_platform"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse("select_platform"), {"platform": "Steam"})
        self.assertRedirects(response, reverse("create-steam-pawn"))

        response = self.client.post(reverse("select_platform"), {"platform": "Switch"})
        self.assertRedirects(response, reverse("create-switch-pawn"))

        response = self.client.post(reverse("select_platform"), {"platform": "Xbox1"})
        self.assertRedirects(response, reverse("create-xbox1-pawn"))

    def test_can_create_pawn_when_logged_in(self):
        steam_pawn_data = self.generate_steam_pawn_data(name="yoshi")

        response = self.client.post(reverse("create-steam-pawn"), steam_pawn_data)
        self.assertEqual(response.status_code, 302)

        created_pawn = SteamPawn.objects.get(**steam_pawn_data)
        self.assertTrue(created_pawn) # If this fails, pawn doesn't exist, which means pawn creation does not work
        self.assertEqual(created_pawn.created_by, self.user)

        switch_pawn_data = self.generate_switch_pawn_data(name="yoshi")

        response = self.client.post(reverse("create-switch-pawn"), switch_pawn_data)
        self.assertEqual(response.status_code, 302)

        created_pawn = SwitchPawn.objects.get(**switch_pawn_data)
        self.assertTrue(created_pawn) # If this fails, pawn doesn't exist, which means pawn creation does not work
        self.assertEqual(created_pawn.created_by, self.user)


        xbox1_pawn_data = self.generate_xbox1_pawn_data(name="xboxer")
        response = self.client.post(reverse("create-xbox1-pawn"), xbox1_pawn_data)
        created_pawn = XboxOnePawn.objects.get(**xbox1_pawn_data)
        self.assertTrue(created_pawn)
        self.assertEqual(created_pawn.created_by, self.user)


class PawnDetailTests(UtilityTestCase):

    def test_detail_view(self):
        response = self.client.get(reverse("view-steam-pawn", kwargs={"pk": self.steam_pawn.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("view-switch-pawn", kwargs={"pk": self.switch_pawn.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("view-xbox1-pawn", kwargs={"pk": self.xbox1_pawn.id}))
        self.assertEqual(response.status_code, 200)

class PawnUpdateTests(UtilityTestCase):

    def test_update_pawn(self):
        steam_pawn_data = self.generate_steam_pawn_data(name=self.test_args["steam_pawn_name"], level=72)
        response = self.client.post(reverse("update-steam-pawn", kwargs={"pk": self.steam_pawn.id}), steam_pawn_data)
        self.assertRedirects(response, reverse("view-steam-pawn", kwargs={"pk": self.steam_pawn.id}))
        self.assertTrue(SteamPawn.objects.get(**steam_pawn_data))

        switch_pawn_data = self.generate_switch_pawn_data(name=self.test_args["switch_pawn_name"], level=75)
        response = self.client.post(reverse("update-switch-pawn", kwargs={"pk": self.switch_pawn.id}), switch_pawn_data)
        self.assertRedirects(response, reverse("view-switch-pawn", kwargs={"pk": self.switch_pawn.id}))
        self.assertTrue(SwitchPawn.objects.get(**switch_pawn_data))

        xbox1_pawn_data = self.generate_xbox1_pawn_data(name=self.test_args["xbox1_pawn_name"], level=80)
        response = self.client.post(reverse("update-xbox1-pawn", kwargs={"pk": self.xbox1_pawn.id}), xbox1_pawn_data)
        self.assertRedirects(response, reverse("view-xbox1-pawn", kwargs={"pk": self.xbox1_pawn.id}))
        self.assertTrue(XboxOnePawn.objects.get(**xbox1_pawn_data))

    def test_403_logged_in_not_owner(self):
        self.create_user_log_in(username="TestUser2")

        steam_pawn_id = self.steam_pawn.id
        response = self.client.get(reverse("update-steam-pawn", kwargs={"pk": steam_pawn_id}))
        self.assertEqual(response.status_code, 403)

        switch_pawn_id = self.switch_pawn.id
        response = self.client.get(reverse("update-switch-pawn", kwargs={"pk": switch_pawn_id}))
        self.assertEqual(response.status_code, 403)

        xbox1_pawn_id = self.xbox1_pawn.id
        response = self.client.get(reverse("update-xbox1-pawn", kwargs={"pk": xbox1_pawn_id}))
        self.assertEqual(response.status_code, 403)


class DeletePawnTests(UtilityTestCase):

    def setUp(self):
        super().setUp()
        self.steam_pawn2 = SteamPawn.objects.create(**self.generate_steam_pawn_data(name="SteamPawn2"))
        self.switch_pawn2 = SwitchPawn.objects.create(**self.generate_switch_pawn_data(name="SwitchPawn2"))
        self.xbox1_pawn2 = XboxOnePawn.objects.create(**self.generate_xbox1_pawn_data(name="XboxOnePawn2"))

    def test_delete_pawn(self):
        response = self.client.post(reverse("delete-steam-pawn", kwargs={"pk": self.steam_pawn.id}))
        self.assertRedirects(response, reverse("manage_pawns"))

        response = self.client.post(reverse("delete-switch-pawn", kwargs={"pk": self.switch_pawn.id}))
        self.assertRedirects(response, reverse("manage_pawns"))

        response = self.client.post(reverse("delete-xbox1-pawn", kwargs={"pk": self.xbox1_pawn.id}))
        self.assertRedirects(response, reverse("manage_pawns"))

    def test_403_logged_in_not_owner(self):
        self.create_user_log_in("TestUser2")
        
        response = self.client.post(reverse("delete-steam-pawn", kwargs={"pk": self.steam_pawn2.id}))
        self.assertEqual(response.status_code, 403)

        response = self.client.post(reverse("delete-switch-pawn", kwargs={"pk": self.switch_pawn2.id}))
        self.assertEqual(response.status_code, 403)

        response = self.client.post(reverse("delete-xbox1-pawn", kwargs={"pk": self.xbox1_pawn2.id}))
        self.assertEqual(response.status_code, 403)