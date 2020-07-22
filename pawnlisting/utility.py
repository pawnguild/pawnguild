from .models import Pawn, SteamPawn, SwitchPawn, XboxOnePawn

base_pawn_fields = ["name", "level", "vocation", "gender", "primary_inclination",
    "secondary_inclination", "tertiary_inclination", "notes", "picture"]

steam_pawn_fields = base_pawn_fields + ["steam_url"]
switch_pawn_fields = base_pawn_fields + ["friend_account_id", "pawn_id"]

class PawnCollection:

    def __init__(self):
        self.steam_pawns = SteamPawn.objects.all()
        self.switch_pawns = SwitchPawn.objects.all()
        self.xbox1_pawns = XboxOnePawn.objects.all()

    def get_context(self):
        return {
            "steam_pawns": self.steam_pawns,
            "switch_pawns": self.switch_pawns,
            "xbox1_pawns": self.xbox1_pawns
        }  

class UserPawnCollection:

    def __init__(self, user):
        self.steam_pawns = SteamPawn.objects.filter(created_by=user)
        self.switch_pawns = SwitchPawn.objects.filter(created_by=user)
        self.xbox1_pawns = XboxOnePawn.objects.filter(created_by=user)

    def get_context(self):
        return {
            "steam_pawns": self.steam_pawns,
            "switch_pawns": self.switch_pawns,
            "xbox1_pawns": self.xbox1_pawns
        }