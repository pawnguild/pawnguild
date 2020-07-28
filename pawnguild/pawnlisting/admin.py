from django.contrib import admin

# Register your models here.
from .models import SteamPawn, SwitchPawn,  XboxOnePawn, PS4Pawn, PS3Pawn

admin.site.register(SteamPawn)
admin.site.register(SwitchPawn)
admin.site.register(XboxOnePawn)
admin.site.register(PS4Pawn)
admin.site.register(PS3Pawn)
