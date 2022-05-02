from django.db.models import Q
from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import View, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    AccessMixin,
)
from django.urls import reverse_lazy

from .models import SteamPawn, SwitchPawn, XboxOnePawn, PS4Pawn, PS3Pawn, vocations
from .forms import (
    SteamPawnForm,
    SwitchPawnForm,
    XboxOnePawnForm,
    PS4PawnForm,
    PS3PawnForm,
    PlatformForm,
)
from .utility import (
    steam_pawn_fields,
    switch_pawn_fields,
    xbox1_pawn_fields,
    ps4_pawn_fields,
    ps3_pawn_fields,
    ManagePawnCollection,
    ListPawnCollection,
    sort_pawns,
    keep_active_pawns,
)


class EmailVerifiedMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.email_verified:
            return redirect(reverse("confirm-account"))
        return super().dispatch(request, *args, **kwargs)


class LimitFivePawnsMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if ManagePawnCollection(request.user).pawn_count() >= 5:
            return redirect(reverse("too-many-pawns"))
        return super().dispatch(request, *args, **kwargs)


class PawnManager(LoginRequiredMixin, EmailVerifiedMixin, TemplateView):
    login_url = "/login/"
    template_name = "pawnlisting/manage_pawns.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pawn_collection = ManagePawnCollection(self.request.user)
        context.update(pawn_collection.get_context())
        return context


class TooManyPawns(TemplateView):
    template_name = "pawnlisting/errors/too_many_pawns.html"


# CreateViews


class AllowPawnCreationMixin(
    LoginRequiredMixin, EmailVerifiedMixin, LimitFivePawnsMixin
):
    pass


class ChoosePawnPlatform(AllowPawnCreationMixin, View):

    login_url = "/login/"

    def get(self, request):
        return render(request, "pawnlisting/pawn_forms/select_platform.html")

    def post(self, request):
        platform_form = PlatformForm(request.POST)
        if platform_form.is_valid():
            platform = platform_form.cleaned_data["platform"]
            if platform == "Steam":
                return redirect(reverse("create-steam-pawn"))
            elif platform == "Switch":
                return redirect(reverse("create-switch-pawn"))
            elif platform == "XboxOne":
                return redirect(reverse("create-xbox1-pawn"))
            elif platform == "PS4":
                return redirect(reverse("create-ps4-pawn"))
            elif platform == "PS3":
                return redirect(reverse("create-ps3-pawn"))
        else:
            return render(
                request,
                "pawnlisting/pawn_forms/select_platform.html",
                context={"platform_form": platform_form},
            )


class CreatePawnMixin(AllowPawnCreationMixin, CreateView):
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


class CreatePS4Pawn(CreatePawnMixin):
    model = PS4Pawn
    form_class = PS4PawnForm
    template_name = "pawnlisting/pawn_forms/ps4.html"


class CreatePS3Pawn(CreatePawnMixin):
    model = PS3Pawn
    form_class = PS3PawnForm
    template_name = "pawnlisting/pawn_forms/ps3.html"


# End CreateViews

# ListViews


class ListAllPawns(View):
    def get(self, request):
        context = ListPawnCollection().get_context()
        return render(
            request, "pawnlisting/list_pawns/list_pawns.html", context=context
        )


def make_ListPawnMixin(Type, origin):
    class ListPawnMixin(ListView):
        def filter_pawns(self, pawns):
            conds = Q()
            if min_level := self.request.GET.get("min-level"):
                conds &= Q(level__gte=min_level)
            if max_level := self.request.GET.get("max-level"):
                conds &= Q(level__lte=max_level)

            # This will show all vocations if someone deselects all vocations,
            # because the cond will be skipped. If they deselect all of them,
            # vocations not in query dict, and we can't know if they came
            # to page normally or through filter
            if vocations := self.request.GET.getlist("vocations"):
                conds &= Q(vocation__in=vocations)

            return pawns.filter(conds)

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context.update({"platform": origin, "vocations": vocations})
            return context

        def get_queryset(self):
            return sort_pawns(keep_active_pawns(self.filter_pawns(Type.objects.all())))

    return ListPawnMixin


class SteamPawnList(make_ListPawnMixin(SteamPawn, "Steam")):
    model = SteamPawn
    context_object_name = "pawns"
    template_name = "pawnlisting/list_pawns/list_steam_pawns.html"


class SwitchPawnList(make_ListPawnMixin(SwitchPawn, "Switch")):
    model = SwitchPawn
    context_object_name = "pawns"
    template_name = "pawnlisting/list_pawns/list_switch_pawns.html"


class XboxOnePawnList(make_ListPawnMixin(XboxOnePawn, "XboxOne")):
    model = XboxOnePawn
    context_object_name = "pawns"
    template_name = "pawnlisting/list_pawns/list_xbox1_pawns.html"


class PS4PawnList(make_ListPawnMixin(PS4Pawn, "PS4")):
    model = PS4Pawn
    context_object_name = "pawns"
    template_name = "pawnlisting/list_pawns/list_ps4_pawns.html"


class PS3PawnList(make_ListPawnMixin(PS3Pawn, "PS3")):
    model = PS3Pawn
    context_object_name = "pawns"
    template_name = "pawnlisting/list_pawns/list_ps3_pawns.html"


# End ListViews

# DetailViews


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


class PS4PawnDetail(PawnDetail):
    model = PS4Pawn
    template_name = "pawnlisting/detail_pawn/ps4.html"


class PS3PawnDetail(PawnDetail):
    model = PS3Pawn
    template_name = "pawnlisting/detail_pawn/ps3.html"


# End DetailViews


def make_UserOwnsPawnMixin(Type):
    """Returns a  Mixin that
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


# UpdateViews


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
    fields = xbox1_pawn_fields
    template_name = "pawnlisting/pawn_forms/xbox1.html"


class PS4PawnUpdate(make_UserOwnsPawnMixin(PS4Pawn), UpdateView):
    model = PS4Pawn
    fields = ps4_pawn_fields
    template_name = "pawnlisting/pawn_forms/ps4.html"


class PS3PawnUpdate(make_UserOwnsPawnMixin(PS3Pawn), UpdateView):
    model = PS3Pawn
    fields = ps3_pawn_fields
    template_name = "pawnlisting/pawn_forms/ps3.html"


# End UpdateViews

# DeleteViews


class DeletePawnMixin(DeleteView):
    success_url = reverse_lazy("manage_pawns")
    template_name = "pawnlisting/pawn_forms/confirm_delete.html"


class SteamPawnDelete(make_UserOwnsPawnMixin(SteamPawn), DeletePawnMixin):
    model = SteamPawn


class SwitchPawnDelete(make_UserOwnsPawnMixin(SwitchPawn), DeletePawnMixin):
    model = SwitchPawn


class XboxOnePawnDelete(make_UserOwnsPawnMixin(XboxOnePawn), DeletePawnMixin):
    model = XboxOnePawn


class PS4PawnDelete(make_UserOwnsPawnMixin(PS4Pawn), DeletePawnMixin):
    model = PS4Pawn


class PS3PawnDelete(make_UserOwnsPawnMixin(PS3Pawn), DeletePawnMixin):
    model = PS3Pawn


# EndDeleteViews
