from datetime import date, timedelta
from html import unescape
import re
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from django.contrib.auth import get_user_model
from django.db import connection
from django.shortcuts import reverse
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.utils import timezone

from pawnguild.pawnlisting.models import (
    SteamPawn,
    SwitchPawn,
    XboxOnePawn,
    PS4Pawn,
    PS3Pawn,
)
from pawnguild.pawnlisting.utility import filter_pawn_activity


class PawnActivityFilterTests(TestCase):
    platforms = (
        ("steam", SteamPawn),
        ("switch", SwitchPawn),
        ("xbox1", XboxOnePawn),
        ("ps4", PS4Pawn),
        ("ps3", PS3Pawn),
    )

    @classmethod
    def setUpTestData(cls):
        cls.owner = get_user_model().objects.create(username="history-test-owner")
        for platform, model in cls.platforms:
            for label, days in (("active", 0), ("year", 180), ("archive", 800)):
                pawn = cls.make_pawn(model, platform + "-" + label)
                model.objects.filter(pk=pawn.pk).update(
                    last_modified=timezone.now() - timedelta(days=days)
                )

    @classmethod
    def make_pawn(cls, model, name, **kwargs):
        values = dict(
            name=name,
            level=50,
            vocation="Mage",
            gender="Female",
            primary_inclination="Nexus",
            created_by=cls.owner,
        )
        values.update(kwargs)
        return model.objects.create(**values)

    def assert_activity_results(self, parameters, labels):
        for platform, model in self.platforms:
            response = self.client.get(
                reverse("list-" + platform + "-pawns"), parameters
            )
            self.assertEqual(response.status_code, 200)
            self.assertCountEqual(
                [p.name for p in response.context["pawns"]],
                [platform + "-" + label for label in labels],
            )
        for url in (reverse("home"), reverse("list-all-pawns")):
            response = self.client.get(url, parameters)
            self.assertEqual(response.status_code, 200)
            for platform, model in self.platforms:
                self.assertCountEqual(
                    [p.name for p in response.context[platform + "_pawns"]],
                    [platform + "-" + label for label in labels],
                )

    def test_existing_default_only_shows_active_pawns(self):
        self.assert_activity_results({}, ["active"])

    def test_year_includes_recent_inactive_pawns_on_every_list(self):
        self.assert_activity_results({"activity": "year"}, ["active", "year"])

    def test_all_time_includes_archive_on_every_list(self):
        self.assert_activity_results({"activity": "all"}, ["active", "year", "archive"])

    def test_invalid_activity_falls_back_to_active(self):
        self.assert_activity_results({"activity": "invalid"}, ["active"])

    def test_active_sql_filter_matches_existing_star_boundaries(self):
        monday = date.today() - timedelta(days=date.today().weekday())
        for offset in (0, 1, 6, 7, 13, 14, 20, 21, 22, 28):
            pawn = self.make_pawn(SteamPawn, "boundary-" + str(offset))
            modified = timezone.now().replace(
                hour=12, minute=0, second=0, microsecond=0
            )
            modified = modified.replace(
                year=monday.year, month=monday.month, day=monday.day
            ) - timedelta(days=offset)
            SteamPawn.objects.filter(pk=pawn.pk).update(last_modified=modified)
            pawn.refresh_from_db()
            matches = filter_pawn_activity(
                SteamPawn.objects.filter(pk=pawn.pk), "active"
            ).exists()
            self.assertEqual(matches, pawn.sunday_based_activity > 0, offset)

    def test_year_boundary_is_inclusive_and_uses_last_modified(self):
        now = timezone.now()
        boundary = now - timedelta(days=365)
        inside = self.make_pawn(SteamPawn, "exact-year")
        outside = self.make_pawn(SteamPawn, "older-than-year")
        SteamPawn.objects.filter(pk=inside.pk).update(last_modified=boundary)
        SteamPawn.objects.filter(pk=outside.pk).update(
            last_modified=boundary - timedelta(microseconds=1)
        )
        with patch("pawnguild.pawnlisting.utility.timezone.now", return_value=now):
            response = self.client.get(
                reverse("list-steam-pawns"), {"activity": "year"}
            )
        ids = [p.pk for p in response.context["pawns"]]
        self.assertIn(inside.pk, ids)
        self.assertNotIn(outside.pk, ids)

    def test_activity_combines_with_level_and_vocation_filters(self):
        matching = self.make_pawn(
            SteamPawn, "matching-archive", level=80, vocation="Fighter"
        )
        SteamPawn.objects.filter(pk=matching.pk).update(
            last_modified=timezone.now() - timedelta(days=800)
        )
        response = self.client.get(
            reverse("list-steam-pawns"),
            {
                "activity": "all",
                "min-level": "70",
                "max-level": "90",
                "vocations": ["Fighter"],
            },
        )
        self.assertEqual([p.pk for p in response.context["pawns"]], [matching.pk])
        self.assertContains(response, 'value="all" selected')
        self.assertContains(response, 'name="min-level" value="70"')
        self.assertEqual(response.context["selected_vocations"], ["Fighter"])

    def test_paginated_links_preserve_repeated_filters_and_stable_order(self):
        for i in range(55):
            self.make_pawn(SteamPawn, "extra-" + str(i))
        params = {
            "activity": "all",
            "min-level": "20",
            "vocations": ["Mage", "Fighter"],
        }
        first = self.client.get(reverse("list-steam-pawns"), params)
        second = self.client.get(reverse("list-steam-pawns"), dict(params, page=2))
        self.assertEqual(len(first.context["pawns"]), 50)
        self.assertEqual(len(second.context["pawns"]), 8)
        first_ids = [p.pk for p in first.context["pawns"]]
        second_ids = [p.pk for p in second.context["pawns"]]
        self.assertFalse(set(first_ids) & set(second_ids))
        self.assertEqual(first_ids + second_ids, sorted(first_ids + second_ids))
        links = [
            parse_qs(urlsplit(unescape(link)).query)
            for link in re.findall(r'href="([^"]+)"', first.content.decode())
        ]
        next_link = next(q for q in links if q.get("page") == ["2"])
        self.assertEqual(next_link["activity"], ["all"])
        self.assertEqual(next_link["min-level"], ["20"])
        self.assertEqual(next_link["vocations"], ["Mage", "Fighter"])

    def test_home_paginates_each_platform_independently(self):
        for i in range(55):
            self.make_pawn(SteamPawn, "extra-" + str(i))
        response = self.client.get(
            reverse("home"), {"activity": "all", "steam-page": "2"}
        )
        self.assertEqual(response.context["steam_pawns"].number, 2)
        self.assertEqual(len(response.context["steam_pawns"]), 8)
        self.assertEqual(len(response.context["switch_pawns"]), 3)
        self.assertContains(response, reverse("list-steam-pawns") + "?activity=all")

    def test_list_requests_do_not_write_pawn_data(self):
        before = list(SteamPawn.objects.values_list("pk", "last_modified"))
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse("home"), {"activity": "all"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            any(
                q["sql"].lstrip().upper().startswith(("INSERT", "UPDATE", "DELETE"))
                for q in queries
            )
        )
        self.assertEqual(
            before, list(SteamPawn.objects.values_list("pk", "last_modified"))
        )
