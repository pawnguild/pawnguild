from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import View, CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError

from .models import Pawn, UserProfile, SteamPawn, SwitchPawn
from .forms import UserProfileForm, SteamPawnForm, SwitchPawnForm
from .utility import *


class Register(View):

    def get(self, request):
        context = { "user_form": UserCreationForm(), "profile_form": UserProfileForm()}
        return render(request, "registration/register.html", context=context)

    def post(self, request):
        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() # Creates a user

            profile = profile_form.save(commit = False)
            profile.user = user
            profile.save()

            login(request, user)
            return redirect(reverse("list-all-pawns"))
        else:
            context = { "user_form": user_form, "profile_form": profile_form}
            return render(request, "registration/register.html", context=context)


class UpdateProfile(LoginRequiredMixin, View):

    def get(self, request):
        context = {"profile_form": UserProfileForm() }
        return render(request, "registration/update_profile.html", context=context)

    def post(self, request):
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse("steam-list-pawn"))
        else:
            context = {"profile_form": profile_form}
            return render(request, "registration/update_profile.html", context=context)


class PawnManager(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    template_name = "pawnlisting/pawn_tables/manage_pawns.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pawn_collection = UserPawnCollection(self.request.user)
        context.update(pawn_collection.get_context())
        return context


### CreateViews ###

class ChoosePawnPlatform(LoginRequiredMixin, View):

    login_url = "/login/"

    def get(self, request):
        return render(request, "pawnlisting/pawn_forms/select_platform.html")

    def post(self, request):
        platform = request.POST["platform"]
        if platform == "Steam":
            return redirect(reverse("create-steam-pawn"))
        elif platform == "Switch":
            return redirect(reverse("create-switch-pawn"))


class CreateSteamPawn(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    model = SteamPawn
    form_class = SteamPawnForm
    template_name = "pawnlisting/pawn_forms/steam.html"

    def form_valid(self, form):
        pawn = form.save(commit=False)
        pawn.created_by = self.request.user
        return super().form_valid(form)


class CreateSwitchPawn(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    model = SwitchPawn
    form_class = SwitchPawnForm
    template_name = "pawnlisting/pawn_forms/switch.html"

    def form_valid(self, form):
        pawn = form.save(commit=False)
        pawn.created_by = self.request.user
        return super().form_valid(form)

### End CreateViews ###

### ListViews ###

class ListAllPawns(View):

    def get(self, request):
        context = PawnCollection().get_context()
        return render(request, "pawnlisting/pawn_tables/list_pawns/list_pawns.html", context=context)


class SteamPawnList(ListView):
    model = SteamPawn
    template_name = "pawnlisting/pawn_tables/list_pawns/list_pawns.html"
    context_object_name = "steam_pawns"

    def get_queryset(self):
        return SteamPawn.objects.all()


class SwitchPawnList(ListView):
    model = SwitchPawn
    template_name = "pawnlisting/pawn_tables/list_pawns/list_pawns.html"
    context_object_name = "switch_pawns"

    def get_queryset(self):
        return SwitchPawn.objects.all()

### End ListViews ###

### DetailViews ###

class PawnDetail(DetailView):
    context_object_name = "pawn"


class SteamPawnDetail(PawnDetail):
    model = SteamPawn
    template_name = "pawnlisting/detail_pawn/steam.html"


class SwitchPawnDetail(PawnDetail):
    model = SwitchPawn
    template_name = "pawnlisting/detail_pawn/switch.html"

### End DetailViews ###


def make_UserOwnsPawnMixin(Type):
    """ Returns a  Mixin that 
        1. Requires login
        2. User passes the following test: they own the Pawn
        3. Applies to any type of Pawn
        """

    class AllowIfUserOwnsPawn(LoginRequiredMixin, UserPassesTestMixin):

        login_url = "/login/"

        def test_func(self):
            pawn_to_delete = Type.objects.get(pk=self.kwargs["pk"])
            return pawn_to_delete.created_by == self.request.user

    return AllowIfUserOwnsPawn


### UpdateViews ###

class SteamPawnUpdate(make_UserOwnsPawnMixin(SteamPawn), UpdateView):
    model = SteamPawn
    fields = steam_pawn_fields
    template_name = "pawnlisting/pawn_forms/steam.html"


class SwitchPawnUpdate(make_UserOwnsPawnMixin(SwitchPawn), UpdateView):
    model = SwitchPawn
    fields = switch_pawn_fields
    template_name = "pawnlisting/pawn_forms/switch.html"

### End UpdateViews ###

### DeleteViews ###

class SteamPawnDelete(make_UserOwnsPawnMixin(SteamPawn), DeleteView):
    model = SteamPawn
    success_url = reverse_lazy("manage_pawns")
    template_name = "pawnlisting/pawn_forms/confirm_delete.html"

class SwitchPawnDelete(make_UserOwnsPawnMixin(SwitchPawn), DeleteView):
    model = SwitchPawn
    success_url = reverse_lazy("manage_pawns")
    template_name = "pawnlisting/pawn_forms/confirm_delete.html"

### EndDeleteViews ###