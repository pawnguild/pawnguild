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

from .models import Pawn, UserProfile


from .forms import PawnForm, UserProfileForm, SteamPawnProfileForm, SwitchPawnProfileForm

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
            return redirect(reverse("list_pawn"))
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
            return redirect(reverse("list_pawn"))
        else:
            context = {"profile_form": profile_form}
            return render(request, "registration/update_profile.html", context=context)


class PawnManager(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    template_name = "pawnlisting/manage_pawns.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_pawns"] = Pawn.objects.filter(created_by=self.request.user)
        return context


class PawnList(ListView):
    model = Pawn
    template_name = "pawnlisting/pawn_list.html"

    def get_queryset(self):
        return Pawn.objects.all()


class PawnDetail(DetailView):
    model = Pawn
    template_name = "pawnlisting/pawn_detail.html"


class GetProfileForms(View):

    def _get_form_and_render(self, request):
        old_post = request.session["_old_post"]


        pawn_form = PawnForm(old_post)
        
        # Creating PawnForm will make errors if any data wasn't filled out
        # They haven't really tried submitting yet, no need to show any errors
        for error in pawn_form.errors: 
            pawn_form.errors[error] = ""

        context = {"form" : pawn_form}

        if pawn_form["platform"] == "Steam":
            context.update({"steam_form": SteamPawnProfileForm(old_post)})
        elif pawn_form["platform"] == "Switch":
            context.update({"switch_form": SwitchPawnProfileForm(old_post)})

        return render(request, "pawnlisting/pawn_form.html", context=context)

    def get(self, request):
        return self._get_form_and_render(request)

    def post(self, request):
        pawn_form = PawnForm(old_post)
        
        # Creating PawnForm will make errors if any data wasn't filled out
        # They haven't really tried submitting yet, no need to show any errors
        for error in pawn_form.errors: 
            pawn_form.errors[error] = ""

        context = {"form" : pawn_form}

        if pawn_form["platform"] == "Steam":
            context.update({"steam_form": SteamPawnProfileForm(old_post)})
        elif pawn_form["platform"] == "Switch":
            context.update({"switch_form": SwitchPawnProfileForm(old_post)})

        return render(request, "pawnlisting/pawn_form.html", context=context)


class PawnCreate(LoginRequiredMixin, View):
    login_url = "/login/"

    model = Pawn
    form_class = PawnForm
    template_name = "pawnlisting/pawn_form.html"

    def get(self, request):
        context = {"form": PawnForm()}
        return render(request, "pawnlisting/pawn_form.html", context=context)

    def post(self, request):
        if "steam_url" in request.POST: # Steam only form field
            pawn_form = PawnForm(request.POST)
            steam_form = SteamPawnProfileForm(request.POST)
            if pawn_form.is_valid() and steam_form.is_valid():
                pawn = pawn_form.save(commit=False)
                pawn.created_by = request.user
                pawn.save()
                steam_profile = steam_form.save(commit=False)
                steam_profile.pawn = pawn
                steam_profile.save()
                return redirect(reverse("list_pawn"))
            else:
                return render(request, "pawnlisting/profile_form.html", context={"pawn_form": pawn_form, "profile_form": steam_form})
        elif "friend_code" in request.POST: # Switch only form field
            pawn_form = PawnForm(request.POST)
            switch_form = SwitchPawnProfileForm(request.POST)
            if pawn_form.is_valid() and switch_form.is_valid():
                pawn = pawn_form.save(commit=False)
                pawn.created_by = request.user
                pawn.save()
                switch_profile = switch_form.save(commit=False)
                switch_profile.pawn = pawn
                switch_profile.save()
                return redirect(reverse("list_pawn"))
        else:
            platform = request.POST["platform"]
            pawn_form = PawnForm(request.POST)
            if pawn_form.is_valid():
                context = {"pawn_form": pawn_form}
                if   platform == "Steam" : context.update({"profile_form" : SteamPawnProfileForm()})
                elif platform == "Switch": context.update({"profile_form" : SwitchPawnProfileForm()})
                return render(request, f"pawnlisting/profile_form.html", context=context)
            else:
                pawn_form = PawnForm(request.POST)
                return render(request, "pawnlisting/pawn_form.html", context={"form": pawn_form})


class AllowIfUserOwnsPawn(LoginRequiredMixin, UserPassesTestMixin):
    login_url = "/login/"

    def test_func(self):
        pawn_to_delete = Pawn.objects.get(pk=self.kwargs["pk"])
        return pawn_to_delete.created_by == self.request.user


class PawnUpdate(AllowIfUserOwnsPawn, UpdateView):
    model = Pawn
    form_class = PawnForm
    success_url = reverse_lazy("manage_pawns")


class PawnDelete(AllowIfUserOwnsPawn, DeleteView):
    model = Pawn
    success_url = reverse_lazy("manage_pawns")

