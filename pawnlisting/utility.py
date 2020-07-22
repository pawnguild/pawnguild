from .models import SteamPawn, SwitchPawn, XboxOnePawn, PS4Pawn, PS3Pawn

base_pawn_fields = ["name", "level", "vocation", "gender", "primary_inclination",
    "secondary_inclination", "tertiary_inclination", "notes", "picture"]

steam_pawn_fields = base_pawn_fields + ["steam_url"]
switch_pawn_fields = base_pawn_fields + ["friend_account_id", "pawn_id"]
xbox1_pawn_fields = base_pawn_fields + ["gamertag"]
ps4_pawn_fields = base_pawn_fields + ["psn"]
ps3_pawn_fields = base_pawn_fields + ["psn", "version"]


class BasePawnCollection:

    def get_context(self):
        return {
            "steam_pawns": self.steam_pawns,
            "switch_pawns": self.switch_pawns,
            "xbox1_pawns": self.xbox1_pawns,
            "ps4_pawns": self.ps4_pawns,
            "ps3_pawns": self.ps3_pawns
        }

class PawnCollection(BasePawnCollection):

    def __init__(self):
        self.steam_pawns = SteamPawn.objects.all()
        self.switch_pawns = SwitchPawn.objects.all()
        self.xbox1_pawns = XboxOnePawn.objects.all()
        self.ps4_pawns = PS4Pawn.objects.all()
        self.ps3_pawns = PS3Pawn.objects.all()

    # def get_context(self):
    #     return {
    #         "steam_pawns": self.steam_pawns,
    #         "switch_pawns": self.switch_pawns,
    #         "xbox1_pawns": self.xbox1_pawns,
    #         "ps4_pawns": self.ps4_pawns,
    #         "ps3_pawns": self.ps3_pawns
    #     }  

class UserPawnCollection(BasePawnCollection):

    def __init__(self, user):
        self.steam_pawns = SteamPawn.objects.filter(created_by=user)
        self.switch_pawns = SwitchPawn.objects.filter(created_by=user)
        self.xbox1_pawns = XboxOnePawn.objects.filter(created_by=user)
        self.ps4_pawns = PS4Pawn.objects.filter(created_by=user)
        self.ps3_pawns = PS3Pawn.objects.filter(created_by=user)

    # def get_context(self):
    #     return {
    #         "steam_pawns": self.steam_pawns,
    #         "switch_pawns": self.switch_pawns,
    #         "xbox1_pawns": self.xbox1_pawns
    #     }