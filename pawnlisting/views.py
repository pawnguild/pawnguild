from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Pawn
    

# Create your views here.
def list_pawn(request):
    pawn_list = Pawn.objects.all()
    context = {"pawn_list": pawn_list}
    return render(request, "pawnlisting/list_pawn.html", context)


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



class PawnForm(CreateView):
    model = Pawn
    fields = ["name", "level", "vocation", "gender",
        "primary_inclination", "secondary_inclination"]


    # def save(self, **kwargs):
    #     self.clean()
    #     return super(Pawn, self).save(**kwargs)