from rest_framework.views import APIView
from rest_framework.response import Response

from .models import SteamPawn, SwitchPawn, PS4Pawn, PS3Pawn, XboxOnePawn
from .serializers import SteamPawnSerializer, SwitchPawnSerializer, XboxOnePawnSerializer, PS4PawnSerializer, PS3PawnSerializer


class SteamPawnAPIList(APIView):
    
    def get(self, request):
        pawns = SteamPawn.objects.all()
        serializer = SteamPawnSerializer(pawns, many=True)
        return Response(serializer.data)


class SwitchPawnAPIList(APIView):

    def get(self, request):
        pawns = SwitchPawn.objects.all()
        serializer = SwitchPawnSerializer(pawns, many=True)
        return Response(serializer.data)


class XboxOnePawnAPIList(APIView):

    def get(self, request):
        pawns = XboxOnePawn.objects.all()
        serializer = XboxOnePawnSerializer(pawns, many=True)
        return Response(serializer.data)


class PS4PawnAPIList(APIView):

    def get(self, request):
        pawns = PS4Pawn.objects.all()
        serializer = PS4PawnSerializer(pawns, many=True)
        return Response(serializer.data)


class PS3PawnAPIList(APIView):

    def get(self, request):
        pawns = PS3Pawn.objects.all()
        serializer = PS3PawnSerializer(pawns, many=True)
        return Response(serializer.data)