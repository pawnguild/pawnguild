from .models import Pawn

from rest_framework import serializers

class PawnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pawn
        fields = "__all__"