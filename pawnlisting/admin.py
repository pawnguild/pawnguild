from django.contrib import admin

# Register your models here.
from .models import Pawn, SteamPawnProfile, SwitchPawnProfile, UserProfile

admin.site.register(Pawn)
admin.site.register(SteamPawnProfile)
admin.site.register(SwitchPawnProfile)
admin.site.register(UserProfile)