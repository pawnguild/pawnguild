from pawnlisting.models import SteamPawn, SwitchPawn, XboxOnePawn, PS4Pawn, PS3Pawn
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

        response = self.client.get(reverse("create-ps4-pawn"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('create-ps4-pawn')}")

        response = self.client.get(reverse("create-ps3-pawn"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('create-ps3-pawn')}")

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

        ps4_pawn_update_url = reverse("update-ps4-pawn", kwargs={"pk": self.ps4_pawn.id})
        response = self.client.get(ps4_pawn_update_url)
        self.assertRedirects(response, f"{reverse('login')}?next={ps4_pawn_update_url}")

        ps3_pawn_update_url = reverse("update-ps3-pawn", kwargs={"pk": self.ps3_pawn.id})
        response = self.client.get(ps3_pawn_update_url)
        self.assertRedirects(response, f"{reverse('login')}?next={ps3_pawn_update_url}")

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

        ps4_pawn_delete_url = reverse("delete-ps4-pawn", kwargs={"pk": self.ps4_pawn.id})
        response = self.client.get(ps4_pawn_delete_url)
        self.assertRedirects(response, f"{reverse('login')}?next={ps4_pawn_delete_url}")

        ps3_pawn_delete_url = reverse("delete-ps3-pawn", kwargs={"pk": self.ps3_pawn.id})
        response = self.client.get(ps3_pawn_delete_url)
        self.assertRedirects(response, f"{reverse('login')}?next={ps3_pawn_delete_url}")


class EmailVerifiedTests(UtilityTestCase):

    def setUp(self):
        super().setUp()
        self.new_user = self.create_user_log_in("TestUser2")
        self.new_user.email_verified = False
        self.new_user.save()
    
    def test_not_verified_redirects(self):
        response = self.client.get(reverse("select_platform"))
        self.assertRedirects(response, reverse("confirm-account"))

        response = self.client.get(reverse("manage_pawns"))
        self.assertRedirects(response, reverse("confirm-account"))


class PawnCreateTests(UtilityTestCase):

    def setUp(self):
        super().setUp()
        self.new_user = self.create_user_log_in("TestUser2")

    def test_pawn_add_no_redirect_logged_in(self):
        response = self.client.get(reverse("select_platform"))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse("select_platform"), {"platform": "Steam"})
        self.assertRedirects(response, reverse("create-steam-pawn"))

        response = self.client.post(reverse("select_platform"), {"platform": "Switch"})
        self.assertRedirects(response, reverse("create-switch-pawn"))

        response = self.client.post(reverse("select_platform"), {"platform": "Xbox1"})
        self.assertRedirects(response, reverse("create-xbox1-pawn"))

        response = self.client.post(reverse("select_platform"), {"platform": "PS4"})
        self.assertRedirects(response, reverse("create-ps4-pawn"))

        response = self.client.post(reverse("select_platform"), {"platform": "PS3"})
        self.assertRedirects(response, reverse("create-ps3-pawn"))

    def test_can_create_pawn_when_logged_in(self):
        steam_pawn_data = self.generate_steam_pawn_data(name="yoshi", created_by=self.new_user)
        response = self.client.post(reverse("create-steam-pawn"), steam_pawn_data)
        self.assertEqual(response.status_code, 302)
        created_pawn = SteamPawn.objects.get(**steam_pawn_data)
        self.assertEqual(created_pawn.created_by, self.new_user)

        switch_pawn_data = self.generate_switch_pawn_data(name="yoshi", created_by=self.new_user)
        response = self.client.post(reverse("create-switch-pawn"), switch_pawn_data)
        self.assertEqual(response.status_code, 302)
        created_pawn = SwitchPawn.objects.get(**switch_pawn_data)
        self.assertEqual(created_pawn.created_by, self.new_user)

        xbox1_pawn_data = self.generate_xbox1_pawn_data(name="xboxer", created_by=self.new_user)
        response = self.client.post(reverse("create-xbox1-pawn"), xbox1_pawn_data)
        created_pawn = XboxOnePawn.objects.get(**xbox1_pawn_data)
        self.assertTrue(created_pawn)
        self.assertEqual(created_pawn.created_by, self.new_user)

        ps4_pawn_data = self.generate_ps4_pawn_data(name="ps4er", created_by=self.new_user)
        response = self.client.post(reverse("create-ps4-pawn"), ps4_pawn_data)
        created_pawn = PS4Pawn.objects.get(**ps4_pawn_data)
        self.assertTrue(created_pawn)
        self.assertEqual(created_pawn.created_by, self.new_user)

        ps3_pawn_data = self.generate_ps3_pawn_data(name="ps3er", created_by=self.new_user)
        response = self.client.post(reverse("create-ps3-pawn"), ps3_pawn_data)
        created_pawn = PS3Pawn.objects.get(**ps3_pawn_data)
        self.assertTrue(created_pawn)
        self.assertEqual(created_pawn.created_by, self.new_user)

        # Limit to 5 Pawns
        ps3_pawn_data = self.generate_ps3_pawn_data(name="AnotherPs3Pawn", created_by=self.new_user)
        response = self.client.post(reverse("create-ps3-pawn"), ps3_pawn_data)
        self.assertRedirects(response, reverse("too-many-pawns"))


class PawnDetailTests(UtilityTestCase):

    def test_detail_view(self):
        response = self.client.get(reverse("view-steam-pawn", kwargs={"pk": self.steam_pawn.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("view-switch-pawn", kwargs={"pk": self.switch_pawn.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("view-xbox1-pawn", kwargs={"pk": self.xbox1_pawn.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("view-ps4-pawn", kwargs={"pk": self.ps4_pawn.id}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("view-ps3-pawn", kwargs={"pk": self.ps3_pawn.id}))
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

        ps4_pawn_data = self.generate_ps4_pawn_data(name=self.test_args["ps4_pawn_name"], level=90)
        response = self.client.post(reverse("update-ps4-pawn", kwargs={"pk": self.ps4_pawn.id}), ps4_pawn_data)
        self.assertRedirects(response, reverse("view-ps4-pawn", kwargs={"pk": self.ps4_pawn.id}))
        self.assertTrue(PS4Pawn.objects.get(**ps4_pawn_data))

        ps3_pawn_data = self.generate_ps3_pawn_data(name=self.test_args["ps3_pawn_name"], level=5)
        response = self.client.post(reverse("update-ps3-pawn", kwargs={"pk": self.ps3_pawn.id}), ps3_pawn_data)
        self.assertRedirects(response, reverse("view-ps3-pawn", kwargs={"pk": self.ps3_pawn.id}))
        self.assertTrue(PS3Pawn.objects.get(**ps3_pawn_data))

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

        ps4_pawn_id = self.ps4_pawn.id
        response = self.client.get(reverse("update-ps4-pawn", kwargs={"pk": ps4_pawn_id}))
        self.assertEqual(response.status_code, 403)

        ps3_pawn_id = self.ps3_pawn.id
        response = self.client.get(reverse("update-ps3-pawn", kwargs={"pk": ps3_pawn_id}))
        self.assertEqual(response.status_code, 403)


class DeletePawnTests(UtilityTestCase):

    def setUp(self):
        super().setUp()
        self.steam_pawn2 = SteamPawn.objects.create(**self.generate_steam_pawn_data(name="SteamPawn2"))
        self.switch_pawn2 = SwitchPawn.objects.create(**self.generate_switch_pawn_data(name="SwitchPawn2"))
        self.xbox1_pawn2 = XboxOnePawn.objects.create(**self.generate_xbox1_pawn_data(name="XboxOnePawn2"))
        self.ps4_pawn2 = PS4Pawn.objects.create(**self.generate_ps4_pawn_data(name="PS4Pawn2"))
        self.ps3_pawn2 = PS3Pawn.objects.create(**self.generate_ps3_pawn_data(name="PS3Pawn2"))

    def test_delete_pawn(self):
        response = self.client.post(reverse("delete-steam-pawn", kwargs={"pk": self.steam_pawn.id}))
        self.assertRedirects(response, reverse("manage_pawns"))

        response = self.client.post(reverse("delete-switch-pawn", kwargs={"pk": self.switch_pawn.id}))
        self.assertRedirects(response, reverse("manage_pawns"))

        response = self.client.post(reverse("delete-xbox1-pawn", kwargs={"pk": self.xbox1_pawn.id}))
        self.assertRedirects(response, reverse("manage_pawns"))

        response = self.client.post(reverse("delete-ps4-pawn", kwargs={"pk": self.ps4_pawn.id}))
        self.assertRedirects(response, reverse("manage_pawns"))

    def test_403_logged_in_not_owner(self):
        self.create_user_log_in("TestUser2")
        
        response = self.client.post(reverse("delete-steam-pawn", kwargs={"pk": self.steam_pawn2.id}))
        self.assertEqual(response.status_code, 403)

        response = self.client.post(reverse("delete-switch-pawn", kwargs={"pk": self.switch_pawn2.id}))
        self.assertEqual(response.status_code, 403)

        response = self.client.post(reverse("delete-xbox1-pawn", kwargs={"pk": self.xbox1_pawn2.id}))
        self.assertEqual(response.status_code, 403)

        response = self.client.post(reverse("delete-ps4-pawn", kwargs={"pk": self.ps4_pawn2.id}))
        self.assertEqual(response.status_code, 403)

        response = self.client.post(reverse("delete-ps3-pawn", kwargs={"pk": self.ps3_pawn2.id}))
        self.assertEqual(response.status_code, 403)