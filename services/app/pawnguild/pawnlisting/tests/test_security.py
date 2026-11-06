from html.parser import HTMLParser

from django.shortcuts import reverse

from pawnguild.pawnlisting.models import SteamPawn
from pawnguild.pawnlisting.tests.utility import UtilityTestCase


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs))


class SteamLinkSecurityTests(UtilityTestCase):
    unsafe_urls = (
        "javascript:alert(1)",
        "data:text/html,test",
        "https://steamcommunity.com/ onmouseover=alert(1)",
        "https://steamcommunity.com/\nonmouseover=alert(1)",
        "https://steamcommunity.com.evil.invalid/id/test",
        "https://steamcommunity.com@evil.invalid/id/test",
        "ftp://steamcommunity.com/id/test",
        "//steamcommunity.com/id/test",
    )

    def test_create_and_update_reject_unsafe_links_without_saving(self):
        # The normal fixture owns five pawns, so free a slot for creation.
        self.ps3_pawn.delete()
        original_url = self.steam_pawn.steam_url
        count = SteamPawn.objects.count()
        for value in self.unsafe_urls:
            for url in (
                reverse("create-steam-pawn"),
                reverse("update-steam-pawn", kwargs={"pk": self.steam_pawn.pk}),
            ):
                with self.subTest(value=value, url=url):
                    data = self.generate_steam_pawn_data("link-test", steam_url=value)
                    response = self.client.post(url, data)
                    self.assertEqual(response.status_code, 200)
                    self.assertIn("steam_url", response.context["form"].errors)
                    self.assertEqual(SteamPawn.objects.count(), count)
                    self.steam_pawn.refresh_from_db()
                    self.assertEqual(self.steam_pawn.steam_url, original_url)

    def test_valid_steam_links_still_work_on_create_and_update(self):
        self.ps3_pawn.delete()
        for value in (
            "https://steamcommunity.com/id/test/",
            "http://steamcommunity.com/profiles/76561198000000000/",
        ):
            with self.subTest(value=value):
                data = self.generate_steam_pawn_data("link-test", steam_url=value)
                response = self.client.post(reverse("create-steam-pawn"), data)
                self.assertEqual(response.status_code, 302)
                created = SteamPawn.objects.exclude(pk=self.steam_pawn.pk).get(
                    name="link-test"
                )
                self.assertEqual(created.steam_url, value)
                created.delete()
                response = self.client.post(
                    reverse("update-steam-pawn", kwargs={"pk": self.steam_pawn.pk}),
                    data,
                )
                self.assertEqual(response.status_code, 302)
                self.steam_pawn.refresh_from_db()
                self.assertEqual(self.steam_pawn.steam_url, value)

    def test_legacy_unsafe_links_are_not_clickable_or_html_attributes(self):
        for value in self.unsafe_urls:
            SteamPawn.objects.filter(pk=self.steam_pawn.pk).update(steam_url=value)
            for url in (
                reverse("view-steam-pawn", kwargs={"pk": self.steam_pawn.pk}),
                reverse("list-steam-pawns"),
                reverse("list-all-pawns"),
            ):
                with self.subTest(value=value, url=url):
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, 200)
                    parser = LinkParser()
                    parser.feed(response.content.decode())
                    for attrs in parser.links:
                        self.assertFalse(any(k.startswith("on") for k in attrs))
                        self.assertNotIn(
                            attrs.get("href", ""),
                            (value, "https://steamcommunity.com/"),
                        )

    def test_valid_link_is_preserved_in_rendered_pages(self):
        response = self.client.get(
            reverse("view-steam-pawn", kwargs={"pk": self.steam_pawn.pk})
        )
        parser = LinkParser()
        parser.feed(response.content.decode())
        link = next(
            a for a in parser.links if a.get("href") == self.steam_pawn.steam_url
        )
        self.assertIn("noopener", link["rel"])
