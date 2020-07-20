from django.test import TestCase
from pawnlisting.models import Pawn
from django.shortcuts import reverse

from pawnlisting.tests.utility import UtilityTestCase

from time import sleep
from datetime import datetime, timedelta

class PawnTests(UtilityTestCase):

    def test_get_absolute_url(self):
        pawn_url = self.pawn.get_absolute_url()
        response = self.client.get(pawn_url)
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(pawn_url, f"/pawn/{self.pawn.id}/")

    def test_last_modified_changes_on_update(self):
        sleep(1) # Allow time to pass so timestamps can change
        pawn_data, profile_data = self.generate_pawn_data(name="T1", platform="Steam", level=51)
        self.client.post(reverse("update_pawn", kwargs={"pk": self.pawn.id}), pawn_data)
        self.assertNotEqual(self.pawn.last_modified, Pawn.objects.get(name="T1").last_modified)

    # def test_activity(self):
#         self.assertEqual(self.created_pawn.activity, 4)

#         pawn = Pawn.objects.get(name="T1")
#         pawn.last_modified = pawn.last_modified - timedelta(days=8)
#         pawn.save()
#         pawn = Pawn.objects.get(name="T1")
#         self.assertEqual(pawn.activity, 3)

class ProfileTests(UtilityTestCase):

    def test_profile_created_with_user(self):
        self.assertTrue(self.user.userprofile) # It exists
        