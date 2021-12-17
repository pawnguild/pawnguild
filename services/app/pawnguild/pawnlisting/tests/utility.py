from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import reverse
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

import random
import string

from pawnguild.pawnlisting.forms import SteamPawnForm, SwitchPawnForm
from pawnguild.pawnlisting.models import (
    SteamPawn,
    SwitchPawn,
    XboxOnePawn,
    PS4Pawn,
    PS3Pawn,
)


class UtilityTestCase(TestCase):
    def setUp(self):
        self.test_args = {
            "test_user": "TestUser",
            "steam_pawn_name": "TestSteamPawn",
            "switch_pawn_name": "TestSwitchPawn",
            "xbox1_pawn_name": "TestXbox1Pawn",
            "ps4_pawn_name": "TestPS4Pawn",
            "ps3_pawn_name": "TestPS3Pawn",
        }

        self.user = self.create_user_log_in(self.test_args["test_user"])
        self.steam_pawn = SteamPawn.objects.create(
            **self.generate_steam_pawn_data(self.test_args["steam_pawn_name"])
        )
        self.switch_pawn = SwitchPawn.objects.create(
            **self.generate_switch_pawn_data(self.test_args["switch_pawn_name"])
        )
        self.xbox1_pawn = XboxOnePawn.objects.create(
            **self.generate_xbox1_pawn_data(self.test_args["xbox1_pawn_name"])
        )
        self.ps4_pawn = PS4Pawn.objects.create(
            **self.generate_ps4_pawn_data(self.test_args["ps4_pawn_name"])
        )
        self.ps3_pawn = PS3Pawn.objects.create(
            **self.generate_ps3_pawn_data(self.test_args["ps3_pawn_name"])
        )

    def generate_pawn_data(
        self,
        name,
        level=50,
        vocation="Mage",
        gender="Male",
        primary_inclination="Nexus",
        secondary_inclination="Pioneer",
        tertiary_inclination="None",
        created_by=None,
    ):

        pawn_data = {
            "name": name,
            "level": level,
            "vocation": vocation,
            "gender": gender,
            "primary_inclination": primary_inclination,
            "secondary_inclination": secondary_inclination,
            "tertiary_inclination": tertiary_inclination,
        }

        creator = created_by or self.user
        pawn_data["created_by"] = creator

        return pawn_data

    def generate_steam_pawn_data(
        self, name, steam_url="https://steamcommunity.com/id/Yellow_Yoshi/", **kwargs
    ):
        steam_data = self.generate_pawn_data(name, **kwargs)
        steam_data["steam_url"] = steam_url
        return steam_data

    def generate_switch_pawn_data(
        self, name, friend_account_id="friend_code", pawn_id="pawn_code", **kwargs
    ):
        switch_data = self.generate_pawn_data(name, **kwargs)
        switch_data["friend_account_id"] = friend_account_id
        switch_data["pawn_id"] = pawn_id
        return switch_data

    def generate_xbox1_pawn_data(self, name, gamertag="MahGamerTag", **kwargs):
        xbox1_data = self.generate_pawn_data(name, **kwargs)
        xbox1_data["gamertag"] = gamertag
        return xbox1_data

    def generate_ps4_pawn_data(self, name, psn="MahPSN", **kwargs):
        ps4_data = self.generate_pawn_data(name, **kwargs)
        ps4_data["psn"] = psn
        return ps4_data

    def generate_ps3_pawn_data(
        self, name, psn="MahPSN3", version="Dark Arisen", **kwargs
    ):
        ps3_data = self.generate_pawn_data(name, **kwargs)
        ps3_data["psn"] = psn
        ps3_data["version"] = version
        return ps3_data

    def create_user_log_in(self, username):
        user, created = get_user_model().objects.get_or_create(username=username)
        user.email = self.random_char(15) + "@gmail.com"
        user.email_verified = True
        user.set_password("12345")
        user.save()

        self.client.login(username=username, password="12345")
        return user

    def test_setup(self):
        self.assertTrue(self.user.is_authenticated)

    def random_char(self, y):
        return "".join(random.choice(string.ascii_letters) for x in range(y))
