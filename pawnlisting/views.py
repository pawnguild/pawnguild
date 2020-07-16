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


from .forms import UserProfileForm

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


class PawnCreate(LoginRequiredMixin, CreateView):
    login_url = "/login/"

    model = Pawn
    fields = ["name", "level", "vocation", "gender",
        "primary_inclination", "secondary_inclination", "notes", "picture"]

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(PawnCreate, self).form_valid(form)


class AllowIfUserOwnsPawn(LoginRequiredMixin, UserPassesTestMixin):
    login_url = "/login/"

    def test_func(self):
        pawn_to_delete = Pawn.objects.get(pk=self.kwargs["pk"])
        return pawn_to_delete.created_by == self.request.user


class PawnUpdate(AllowIfUserOwnsPawn, UpdateView):
    model = Pawn
    fields = ["name", "level", "vocation", "gender",
        "primary_inclination", "secondary_inclination", "notes", "picture"]


class PawnDelete(AllowIfUserOwnsPawn, DeleteView):
    model = Pawn
    success_url = reverse_lazy("list_pawn")

