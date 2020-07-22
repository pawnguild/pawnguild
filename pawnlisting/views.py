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

from .models import UserProfile, SteamPawn, SwitchPawn, XboxOnePawn
from .forms import UserProfileForm, SteamPawnForm, SwitchPawnForm, XboxOnePawnForm
from .utility import *


class Register(View):

    def get(self, request):
        context = {"profile_form": UserProfileForm()}
        return render(request, "registration/register.html", context=context)

    def post(self, request):
        profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():
            user = profile_form.save() # Creates a user
            login(request, user)
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
            return redirect(reverse("list-all-pawns"))
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
        elif platform == "Xbox1":
            return redirect(reverse("create-xbox1-pawn"))

class CreatePawnMixin(LoginRequiredMixin, CreateView):
    login_url = "/login/"

    def form_valid(self, form):
        pawn = form.save(commit=False)
        pawn.created_by = self.request.user
        return super().form_valid(form)


class CreateSteamPawn(CreatePawnMixin):
    model = SteamPawn
    form_class = SteamPawnForm
    template_name = "pawnlisting/pawn_forms/steam.html"


class CreateSwitchPawn(CreatePawnMixin):
    model = SwitchPawn
    form_class = SwitchPawnForm
    template_name = "pawnlisting/pawn_forms/switch.html"


class CreateXboxOnePawn(CreatePawnMixin):
    model = XboxOnePawn
    form_class = XboxOnePawnForm
    template_name = "pawnlisting/pawn_forms/xbox1.html"


### End CreateViews ###

### ListViews ###

class ListAllPawns(View):

    def get(self, request):
        context = PawnCollection().get_context()
        return render(request, "pawnlisting/pawn_tables/list_pawns/list_pawns.html", context=context)


def make_ListPawnMixin(Type):

    class ListPawnMixin(ListView):
        template_name = "pawnlisting/pawn_tables/list_pawns/list_pawns.html"

        def get_queryset(self):
            return Type.objects.all()
    
    return ListPawnMixin


class SteamPawnList(make_ListPawnMixin(SteamPawn)):
    model = SteamPawn
    context_object_name = "steam_pawns"


class SwitchPawnList(make_ListPawnMixin(SwitchPawn)):
    model = SwitchPawn
    context_object_name = "switch_pawns"


class XboxOnePawnList(make_ListPawnMixin(XboxOnePawn)):
    model = XboxOnePawn
    context_object_name = "xbox1_pawns"


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


class XboxOnePawnDetail(PawnDetail):
    model = XboxOnePawn
    template_name = "pawnlisting/detail_pawn/xbox1.html"

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


class XboxOnePawnUpdate(make_UserOwnsPawnMixin(XboxOnePawn), UpdateView):
    model = XboxOnePawn
    fields = base_pawn_fields
    template_name = "pawnlisting/pawn_forms/xbox1.html"

### End UpdateViews ###

### DeleteViews ###


class DeletePawnMixin(DeleteView):
    success_url = reverse_lazy("manage_pawns")
    template_name = "pawnlisting/pawn_forms/confirm_delete.html"


class SteamPawnDelete(make_UserOwnsPawnMixin(SteamPawn), DeletePawnMixin):
    model = SteamPawn


class SwitchPawnDelete(make_UserOwnsPawnMixin(SwitchPawn), DeletePawnMixin):
    model = SwitchPawn


class XboxOnePawnDelete(make_UserOwnsPawnMixin(XboxOnePawn), DeletePawnMixin):
    model = XboxOnePawn


### EndDeleteViews ###