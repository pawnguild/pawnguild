from django.test import TestCase, Client
from pawnlisting.models import Pawn
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import reverse



class CreatePawnTests(TestCase):

    def setUp(self):
        self.client = Client()

    def generate_pawn_data(self, name="T1", level=50, vocation="Mage", gender="Male", primary_inclination="Nexus", secondary_inclination="Pioneer"):
        return {"name": name, "level": level, "vocation": vocation, "gender": gender,
            "primary_inclination": primary_inclination, "secondary_inclination": secondary_inclination}

    def create_user_log_in(self):
        user = get_user_model().objects.create(username="testuser")
        user.set_password("12345")
        user.save()
        self.client.login(username="testuser", password="12345")

    def test_pawn_add_redirects_not_logged_in(self):
        response = self.client.get(reverse("create_pawn"))
        self.assertRedirects(response, "/login/?next=/add_pawn/")

    def test_cannot_create_pawn_when_not_logged_in(self):
        response = self.client.post(reverse("create_pawn"), self.generate_pawn_data("T1"))
        self.assertRedirects(response, "/login/?next=/add_pawn/")

    def test_pawn_add_no_redirect_logged_in(self):
        self.create_user_log_in()
        response = self.client.get(reverse("create_pawn"))
        self.assertEqual(response.status_code, 200)

    def test_can_create_pawn_when_logged_in(self):
        self.create_user_log_in()
        pawn_data = self.generate_pawn_data(name="yoshi")
        response = self.client.post(reverse("create_pawn"), pawn_data)
        self.assertRedirects(response, "/list/")
        pawn = Pawn.objects.get(**pawn_data)
        self.assertTrue(pawn) # If this fails, pawn doesn't exist, which means pawn creation does not work