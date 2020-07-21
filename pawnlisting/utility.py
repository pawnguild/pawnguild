from .models import Pawn, SteamPawn, SwitchPawn

class UserPawnCollection:

    def __init__(self, user):
        self.steam_pawns = SteamPawn.objects.filter(created_by=user)
        self.switch_pawns = SwitchPawn.objects.filter(created_by=user)

    def get_context(self):
        return {
            "steam_pawns": self.steam_pawns,
            "switch_pawns": self.switch_pawns
        }