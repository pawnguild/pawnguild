from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import reverse
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

from pawnlisting.forms import UserProfileForm, SteamPawnForm, SwitchPawnForm
from pawnlisting.models import SteamPawn, SwitchPawn

class UtilityTestCase(TestCase):

    def setUp(self):
        self.test_args = {"test_user": "TestUser", 
                            "steam_pawn_name": "TestSteamPawn",
                            "switch_pawn_name": "TestSwitchPawn"}

        self.user = self.register_user_log_in(self.test_args["test_user"])
        self.steam_pawn = SteamPawn.objects.create(**self.generate_steam_pawn_data(self.test_args["steam_pawn_name"]))
        self.switch_pawn  = SwitchPawn.objects.create(**self.generate_switch_pawn_data(self.test_args["switch_pawn_name"]))

    def generate_pawn_data(self, name, level=50, vocation="Mage", gender="Male", primary_inclination="Nexus",
                            secondary_inclination="Pioneer", tertiary_inclination="None", created_by=None):

        pawn_data = {"name": name, "level": level, "vocation": vocation, "gender": gender,
            "primary_inclination": primary_inclination, "secondary_inclination": secondary_inclination,
            "tertiary_inclination": tertiary_inclination}

        creator = created_by or self.user
        pawn_data["created_by"] = creator

        return pawn_data

    def generate_steam_pawn_data(self, name, steam_url="https://steamcommunity.com/id/Yellow_Yoshi/", **kwargs):
        steam_data = self.generate_pawn_data(name, **kwargs)
        steam_data["steam_url"] = steam_url
        return steam_data

    def generate_switch_pawn_data(self, name, friend_code="friend_code", pawn_code="pawn_code", **kwargs):
        switch_data = self.generate_pawn_data(name, **kwargs)
        switch_data["friend_code"] = friend_code
        switch_data["pawn_code"] = pawn_code
        return switch_data

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
        except get_user_model().DoesNotExist as e:
            pass

        user_creation_form_data = {"username": username, "password1": "testpassword", 
                                                         "password2": "testpassword"}
        data = user_creation_form_data

        response = self.client.post(reverse("register"), data=data)
        user = auth.get_user(self.client)
        return user

    def test_setup(self):
        self.assertTrue(self.user.is_authenticated)
