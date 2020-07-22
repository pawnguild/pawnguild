from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm

class UserProfileForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = UserCreationForm.Meta.fields + ("email",)