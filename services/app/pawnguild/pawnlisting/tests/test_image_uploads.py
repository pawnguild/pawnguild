from io import BytesIO
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import reverse
from PIL import Image, features

from pawnguild.pawnlisting.models import SteamPawn
from pawnguild.pawnlisting.tests.utility import UtilityTestCase


class PawnImageUploadTests(UtilityTestCase):
    def test_webp_decoder_includes_the_security_fix(self):
        version = features.version("webp")
        self.assertIsNotNone(version)
        self.assertGreaterEqual(tuple(map(int, version.split("."))), (1, 3, 2))

    def image_upload(self, format):
        contents = BytesIO()
        Image.new("RGB", (8, 8), "blue").save(contents, format=format)
        return SimpleUploadedFile(
            "pawn." + format.lower(), contents.getvalue(), "image/" + format.lower()
        )

    def test_common_picture_formats_can_be_created_updated_and_read(self):
        self.ps3_pawn.delete()
        for format in ("PNG", "JPEG", "GIF", "WEBP"):
            with self.subTest(format=format):
                data = self.generate_steam_pawn_data("image-test")
                data["picture"] = self.image_upload(format)
                response = self.client.post(reverse("create-steam-pawn"), data)
                self.assertEqual(response.status_code, 302)
                pawn = SteamPawn.objects.get(name="image-test")
                with Image.open(pawn.picture.path) as picture:
                    picture.load()
                    self.assertEqual(picture.size, (8, 8))
                    self.assertEqual(picture.format, format)
                data["picture"] = self.image_upload(format)
                response = self.client.post(
                    reverse("update-steam-pawn", kwargs={"pk": pawn.pk}), data
                )
                self.assertEqual(response.status_code, 302)
                pawn.refresh_from_db()
                with Image.open(pawn.picture.path) as picture:
                    picture.load()
                    self.assertEqual(picture.size, (8, 8))
                pawn.delete()

    def test_invalid_image_is_rejected_without_changing_existing_pawn(self):
        data = self.generate_steam_pawn_data("changed-name")
        data["picture"] = SimpleUploadedFile(
            "fake.png", b"This is not an image", "image/png"
        )
        response = self.client.post(
            reverse("update-steam-pawn", kwargs={"pk": self.steam_pawn.pk}), data
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("picture", response.context["form"].errors)
        self.steam_pawn.refresh_from_db()
        self.assertEqual(self.steam_pawn.name, self.test_args["steam_pawn_name"])

    def test_only_owner_can_delete_pawn_and_its_picture(self):
        self.steam_pawn.picture.save("owner-only.png", self.image_upload("PNG"))
        picture = Path(self.steam_pawn.picture.path)
        url = reverse("delete-steam-pawn", kwargs={"pk": self.steam_pawn.pk})
        self.create_user_log_in("other-owner")
        self.assertEqual(self.client.post(url).status_code, 403)
        self.assertTrue(picture.exists())
        self.assertTrue(SteamPawn.objects.filter(pk=self.steam_pawn.pk).exists())
        self.client.login(username=self.user.username, password="12345")
        self.assertRedirects(self.client.post(url), reverse("manage_pawns"))
        self.assertFalse(SteamPawn.objects.filter(pk=self.steam_pawn.pk).exists())
        self.assertFalse(picture.exists())
        self.assertEqual(self.user.switchpawn_set.count(), 1)
