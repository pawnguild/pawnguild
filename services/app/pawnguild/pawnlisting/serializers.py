from .models import SteamPawn, SwitchPawn, PS4Pawn, PS3Pawn, XboxOnePawn
from .utility import (
    steam_pawn_fields,
    switch_pawn_fields,
    xbox1_pawn_fields,
    ps4_pawn_fields,
    ps3_pawn_fields,
)

from rest_framework import serializers

# steam_pawn_fields = base_pawn_fields + ["steam_url"]
# switch_pawn_fields = base_pawn_fields + ["friend_account_id", "pawn_id"]
# xbox1_pawn_fields = base_pawn_fields + ["gamertag"]
# ps4_pawn_fields = base_pawn_fields + ["psn"]
# ps3_pawn_fields = base_pawn_fields + ["psn", "version"]


class SteamPawnSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteamPawn
        fields = steam_pawn_fields


class SwitchPawnSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwitchPawn
        fields = switch_pawn_fields


class XboxOnePawnSerializer(serializers.ModelSerializer):
    class Meta:
        model = XboxOnePawn
        fields = xbox1_pawn_fields


class PS4PawnSerializer(serializers.ModelSerializer):
    class Meta:
        model = PS4Pawn
        fields = ps4_pawn_fields


class PS3PawnSerializer(serializers.ModelSerializer):
    class Meta:
        model = PS3Pawn
        fields = ps3_pawn_fields
