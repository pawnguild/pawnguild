from datetime import date, timedelta

from django.core.paginator import Paginator
from django.db.models import Case, IntegerField, Value, When
from django.utils import timezone

from .models import SteamPawn, SwitchPawn, XboxOnePawn, PS4Pawn, PS3Pawn


base_pawn_fields = [
    "name",
    "level",
    "vocation",
    "gender",
    "primary_inclination",
    "secondary_inclination",
    "tertiary_inclination",
    "notes",
    "picture",
    "primary_skills",
    "secondary_skills",
]

steam_pawn_fields = base_pawn_fields + ["steam_url"]
switch_pawn_fields = base_pawn_fields + ["friend_account_id", "pawn_id"]
xbox1_pawn_fields = base_pawn_fields + ["gamertag"]
ps4_pawn_fields = base_pawn_fields + ["psn"]
ps3_pawn_fields = base_pawn_fields + ["psn", "version"]

platforms = ["Steam", "Switch", "XboxOne", "PS4", "PS3"]


ACTIVITY_CHOICES = (
    ("active", "Currently active"),
    ("year", "Updated within the last year"),
    ("all", "All time"),
)
PAWNS_PER_PAGE = 50


def normalize_activity(value):
    return value if value in dict(ACTIVITY_CHOICES) else "active"


def filter_pawn_activity(pawns, activity):
    activity = normalize_activity(activity)
    if activity == "year":
        return pawns.filter(last_modified__gte=timezone.now() - timedelta(days=365))
    if activity == "all":
        return pawns
    # Match Pawn.sunday_based_activity: stars expire 21 days before this Monday.
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    return pawns.filter(last_modified__date__gte=monday - timedelta(days=20))


def order_list_pawns(pawns):
    # Sort in SQL before paginating, retaining the existing vocation/level order.
    order = ["Fighter", "Warrior", "Strider", "Ranger", "Mage", "Sorcerer"]
    return pawns.order_by(
        Case(
            *[
                When(vocation=vocation, then=Value(i))
                for i, vocation in enumerate(order)
            ],
            default=Value(len(order)),
            output_field=IntegerField(),
        ),
        "level",
        "pk",
    )


def keep_active_pawns(pawns):
    return filter(lambda p: p.sunday_based_activity > 0, pawns)


def sort_pawns(pawns):
    vocation_order = {
        "Fighter": 0,
        "Warrior": 1,
        "Strider": 2,
        "Ranger": 3,
        "Mage": 4,
        "Sorcerer": 5,
    }
    return sorted(pawns, key=lambda pawn: (vocation_order[pawn.vocation], pawn.level))


class BasePawnCollection:
    def get_context(self):
        return {
            "steam_pawns": sort_pawns(self.steam_pawns),
            "switch_pawns": sort_pawns(self.switch_pawns),
            "xbox1_pawns": sort_pawns(self.xbox1_pawns),
            "ps4_pawns": sort_pawns(self.ps4_pawns),
            "ps3_pawns": sort_pawns(self.ps3_pawns),
        }


class ListPawnCollection:
    def __init__(self, activity="active", pages=None):
        self.activity = normalize_activity(activity)
        self.pages = pages or {}

    def get_context(self):
        context = {"activity": self.activity, "activity_choices": ACTIVITY_CHOICES}
        for platform, model in (
            ("steam", SteamPawn),
            ("switch", SwitchPawn),
            ("xbox1", XboxOnePawn),
            ("ps4", PS4Pawn),
            ("ps3", PS3Pawn),
        ):
            pawns = order_list_pawns(
                filter_pawn_activity(model.objects.all(), self.activity)
            )
            context[f"{platform}_pawns"] = Paginator(pawns, PAWNS_PER_PAGE).get_page(
                self.pages.get(f"{platform}-page")
            )
        return context


class ManagePawnCollection(BasePawnCollection):
    def __init__(self, user):
        self.steam_pawns = SteamPawn.objects.filter(created_by=user)
        self.switch_pawns = SwitchPawn.objects.filter(created_by=user)
        self.xbox1_pawns = XboxOnePawn.objects.filter(created_by=user)
        self.ps4_pawns = PS4Pawn.objects.filter(created_by=user)
        self.ps3_pawns = PS3Pawn.objects.filter(created_by=user)

    def pawn_count(self):
        # Flake and black disagree on how to format
        # binary operators with newlines
        return (
            len(self.steam_pawns)
            + len(self.switch_pawns)  # noqa: W503
            + len(self.xbox1_pawns)  # noqa: W503
            + len(self.ps4_pawns)  # noqa: W503
            + len(self.ps3_pawns)  # noqa: W503
        )
