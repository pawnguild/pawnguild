from django.test import TestCase, Client
from pawnlisting.models import Pawn
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import reverse

from crum import get_current_user, impersonate

from pawnlisting.tests.utility import Utility

from time import sleep

class PawnTests(Utility, TestCase):

    def setUp(self):
        user = self.create_user_log_in("testuser")
        with impersonate(user):
            self.created_pawn = Pawn.objects.create(**self.generate_pawn_data(name="T1", level=50))

    def test_pawn_creation_created_by(self):
        t1 = Pawn.objects.get(name="T1")
        self.assertEqual(t1.created_by.username, "testuser")

    def test_get_absolute_url(self):
        pawn_url = self.created_pawn.get_absolute_url()
        response = self.client.get(pawn_url)
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(pawn_url, f"/pawn/{self.created_pawn.id}/")

    def test_last_modified_changes_on_update(self):
        sleep(1) # Allow time to pass so timestamps can change
        self.client.post(reverse("update_pawn", kwargs={"pk": self.created_pawn.id}), self.generate_pawn_data(name="T1", level=51))
        self.assertNotEqual(self.created_pawn.last_modified, Pawn.objects.get(name="T1").last_modified)