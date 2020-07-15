from django.contrib import admin

# Register your models here.
from .models import Pawn, UserProfile

admin.site.register(Pawn)
admin.site.register(UserProfile)