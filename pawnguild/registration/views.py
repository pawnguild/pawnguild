from django.shortcuts import render
from django.views.generic.edit import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView

from django.contrib.auth.views import LoginView

from .forms import UserProfileCreationForm

from django_email_verification import sendConfirm

# Create your views here.


class Login(LoginView):
    pass


class Register(View):

    def get(self, request):
        context = {"form": UserProfileCreationForm()}
        return render(request, "registration/register.html", context=context)

    def post(self, request):
        profile_form = UserProfileCreationForm(request.POST)
        if profile_form.is_valid():
            user = profile_form.save() # Creates a user
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            sendConfirm(user)
            return render(request, "registration/confirm_account_sent.html", context={"email": request.user.email})
        else:
            context = {"profile_form": profile_form}
            return render(request, "registration/register.html", context=context)


class UpdateProfile(LoginRequiredMixin, View):

    def get(self, request):
        context = {"profile_form": UserProfileCreationForm() }
        return render(request, "registration/update_profile.html", context=context)

    def post(self, request):
        profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse("pawnlisting/list-all-pawns"))
        else:
            context = {"profile_form": profile_form}
            return render(request, "registration/update_profile.html", context=context)

class ConfirmAccount(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, "registration/confirm_account_send.html", context={"email": request.user.email})

    def post(self, request):
        sendConfirm(self.request.user)
        return render(request, "registration/confirm_account_sent.html", context={"email": request.user.email})