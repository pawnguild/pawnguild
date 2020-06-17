from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Pawn

from django.urls import reverse_lazy
    

class Register(TemplateView):
    template_view = "registration/register.html"

    def get(self, request):
        context = { "form": UserCreationForm() }
        return render(request, "registration/register.html", context=context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # Creates a user
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"] # verified box is pw2
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse("list_pawn"))
        else:
            HttpResponseRedirect(reverse("register"))


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
        "primary_inclination", "secondary_inclination"]


class AllowIfUserOwnsPawn(UserPassesTestMixin):

    def test_func(self):
        pawn_to_delete = Pawn.objects.get(pk=self.kwargs["pk"])
        return pawn_to_delete.created_by == self.request.user

class PawnUpdate(AllowIfUserOwnsPawn, UpdateView):
    model = Pawn
    fields = ["name", "level", "vocation", "gender",
        "primary_inclination", "secondary_inclination"]


class PawnDelete(AllowIfUserOwnsPawn, DeleteView):
    model = Pawn
    success_url = reverse_lazy("list_pawn")


