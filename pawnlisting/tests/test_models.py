from django.test import TestCase, Client
from pawnlisting.models import Pawn
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import reverse

from crum import get_current_user, impersonate

from pawnlisting.tests.utility import Utility

class PawnTests(Utility, TestCase):

    def setUp(self):
        user = get_user_model().objects.create(username="testuser")
        user.set_password("12345")
        user.save()
        with impersonate(user):
            self.created_pawn = Pawn.objects.create(name="T1", level=50, vocation="Mage", gender="Male", primary_inclination="Scathar", secondary_inclination="Nexus")

    def test_pawn_creation_created_by(self):
        t1 = Pawn.objects.get(name="T1")
        self.assertEqual(t1.created_by.username, "testuser")

    def test_get_absolute_url(self):
        pawn_url = self.created_pawn.get_absolute_url()
        response = self.client.get(pawn_url)
        self.assertEqual(response.status_code, 200)
        self.assertURLEqual(pawn_url, f"/pawn/{self.created_pawn.id}/")
