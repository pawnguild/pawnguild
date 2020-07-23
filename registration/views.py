from django.shortcuts import render
from django.views.generic.edit import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, reverse, redirect

from .forms import UserProfileForm

from django_email_verification import sendConfirm

# Create your views here.

class Register(View):

    def get(self, request):
        context = {"profile_form": UserProfileForm()}
        return render(request, "registration/register.html", context=context)

    def post(self, request):
        profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():
            user = profile_form.save() # Creates a user
            login(request, user)
            sendConfirm(user)
            return redirect(reverse("list-all-pawns"))
        else:
            context = {"profile_form": profile_form}
            return render(request, "registration/register.html", context=context)


class UpdateProfile(LoginRequiredMixin, View):

    def get(self, request):
        context = {"profile_form": UserProfileForm() }
        return render(request, "registration/update_profile.html", context=context)

    def post(self, request):
        profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse("pawnlisting/list-all-pawns"))
        else:
            context = {"profile_form": profile_form}
            return render(request, "registration/update_profile.html", context=context)
