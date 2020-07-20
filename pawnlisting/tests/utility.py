from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import reverse
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

from pawnlisting.forms import UserProfileForm, SteamPawnProfileForm, SwitchPawnProfileForm
from pawnlisting.models import Pawn, SteamPawnProfile, SwitchPawnProfile

pawn_profiles = {SteamPawnProfile: SteamPawnProfileForm, SwitchPawnProfile: SwitchPawnProfileForm}



class UtilityTestCase(TestCase):

    def setUp(self):
        self.user = self.register_user_log_in("TestUser")
        self.create_args = [self.user, "TestPawn", "Steam"]
        self.pawn, self.pawn_profile = self.createPawnAndProfile(*self.create_args)

    def createPawnAndProfile(self, user, pawn_name, platform):
        pawn_data, pawn_profile_data = self.generate_pawn_data(name=pawn_name, platform=platform)
        pawn = Pawn.objects.create(**pawn_data)
        
        for Profile, ProfileForm in pawn_profiles.items():
            profile_form = ProfileForm(pawn_profile_data)
            if profile_form.is_valid():
                pawn_profile = profile_form.save(commit=False)
                pawn_profile.pawn = pawn
                pawn_profile.save()

        return pawn, pawn_profile

    def generate_pawn_data(self, name, level=50, vocation="Mage", gender="Male", primary_inclination="Nexus",
                                secondary_inclination="Pioneer", tertiary_inclination="None", platform="Steam", created_by=None):
        pawn_data = {"name": name, "level": level, "vocation": vocation, "gender": gender,
            "primary_inclination": primary_inclination, "secondary_inclination": secondary_inclination,
            "tertiary_inclination": tertiary_inclination, "platform": platform}
        if created_by:
            pawn_data.update({"created_by": created_by})
        else:
            pawn_data.update({"created_by": self.user})
        profile_data = {}
        if platform == "Steam":
            profile_data["steam_url"] = "https://steamcommunity.com/id/Yellow_Yoshi/"
        elif platform == "Switch":
            profile_data["friend_code"] = "friend code"
            profile_data["pawn_code"] = "pawn code"
        return pawn_data, profile_data

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
        except User.DoesNotExist as e:
            pass

        user_creation_form_data = {"username": username, "password1": "testpassword", 
                                                         "password2": "testpassword"}
        profile_form_data = {"steam_url": "https://steamcommunity.com/id/Yellow_Yoshi/"}
        data = {**user_creation_form_data, **profile_form_data}

        response = self.client.post(reverse("register"), data=data)
        user = auth.get_user(self.client)
        return user

    def test_setup(self):
        self.assertTrue(self.user.is_authenticated)
