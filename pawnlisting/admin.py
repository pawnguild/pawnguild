from django.contrib import admin

# Register your models here.
from .models import SteamPawn, SwitchPawn,  XboxOnePawn, UserProfile

admin.site.register(SteamPawn)
admin.site.register(SwitchPawn)
admin.site.register(XboxOnePawn)
admin.site.register(UserProfile)