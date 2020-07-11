from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Pawn
from .serializers import PawnSerializer

class PawnAPIList(APIView):
    
    def get(self, request):
        """ List all pawns """
        pawns = Pawn.objects.all()
        serializer = PawnSerializer(pawns, many=True)
        return Response(serializer.data)