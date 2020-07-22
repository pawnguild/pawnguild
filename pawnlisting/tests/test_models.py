from django.test import TestCase
from pawnlisting.models import SteamPawn, SwitchPawn
from django.shortcuts import reverse

from pawnlisting.tests.utility import UtilityTestCase

from time import sleep
from datetime import datetime, timedelta

class PawnTests(UtilityTestCase):

    def test_get_absolute_url(self):
        steam_pawn_url = self.steam_pawn.get_absolute_url()
        response = self.client.get(steam_pawn_url)
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(steam_pawn_url, f"/pawn/steam/{self.steam_pawn.id}/")

        switch_pawn_url = self.switch_pawn.get_absolute_url()
        response = self.client.get(switch_pawn_url)
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(switch_pawn_url, f"/pawn/switch/{self.switch_pawn.id}/")

    def test_last_modified_changes_on_update(self):
        sleep(1) # Allow time to pass so timestamps can change
        steam_pawn_data = self.generate_steam_pawn_data(name="T1", level=51)
        self.client.post(reverse("update-steam-pawn", kwargs={"pk": self.steam_pawn.id}), steam_pawn_data)
        self.assertNotEqual(self.steam_pawn.last_modified, SteamPawn.objects.get(name="T1").last_modified)

    # def test_activity(self):
        # self.assertEqual(self.created_pawn.activity, 4)

        # pawn = Pawn.objects.get(name="T1")
        # pawn.last_modified = pawn.last_modified - timedelta(days=8)
        # pawn.save()
        # pawn = Pawn.objects.get(name="T1")
        # self.assertEqual(pawn.activity, 3)

class ProfileTests(UtilityTestCase):

    def test_profile_created_with_user(self):
        self.assertTrue(self.user.userprofile) # It exists
        