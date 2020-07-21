from .models import Pawn, SteamPawnProfile, SwitchPawnProfile
from .forms import SteamPawnProfileForm, SwitchPawnProfileForm

def get_pawn_profile(pawn: Pawn):
    profile = None
    try:
        profile = pawn.steampawnprofile
    except SteamPawnProfile.DoesNotExist:
        pass
    try:
        profile = pawn.switchpawnprofile
    except SwitchPawnProfile.DoesNotExist:
        pass

    if profile == None:
        raise Exception("Pawn profile could not be found")
    return profile


def get_profile_form(pawn: Pawn):
    if pawn.platform == "Steam":
        return SteamPawnProfileForm
    elif pawn.platform == "Switch":
        return SwitchPawnProfileForm