from django.contrib.auth import get_user_model
from django.test import TestCase
from django.shortcuts import reverse
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

from pawnlisting.forms import UserProfileForm
from pawnlisting.models import Pawn

class UtilityTestCase(TestCase):

    def setUp(self):
        self.user = self.register_user_log_in("TestUser")
        self.pawn_data = {**self.generate_pawn_data(name="TestPawn"), "created_by": self.user}
        self.pawn = Pawn.objects.create(**self.pawn_data)

    def generate_pawn_data(self, name, level=50, vocation="Mage", gender="Male", primary_inclination="Nexus", secondary_inclination="Pioneer"):
        return {"name": name, "level": level, "vocation": vocation, "gender": gender,
            "primary_inclination": primary_inclination, "secondary_inclination": secondary_inclination}

    def create_user_log_in(self, username):
        user, created = get_user_model().objects.get_or_create(username=username)
        user.set_password("12345")
        user.save()
    
        self.client.login(username=username, password="12345")
        return user

    def register_user_log_in(self, username):
        try:
            user = get_user_model().objects.get(username=username)
            return user
        except Exception as e:
            print(str(e))

        user_creation_form_data = {"username": username, "password1": "testpassword", 
                                                         "password2": "testpassword"}
        profile_form_data = {"steam_url": "https://steamcommunity.com/id/Yellow_Yoshi/"}
        data = {**user_creation_form_data, **profile_form_data}

        response = self.client.post(reverse("register"), data=data)
        user = auth.get_user(self.client)
        return user

        def test_setup(self):
            self.assertTrue(self.user.is_authenticated)
