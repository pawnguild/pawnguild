from django.shortcuts import reverse

from pawnguild.pawnlisting.tests.utility import UtilityTestCase


class TestPawnApi(UtilityTestCase):
    def test_pawn_list_api(self):
        self.client.logout()
        for platform, account_field in (
            ("steam", "steam_url"),
            ("switch", "friend_account_id"),
            ("xbox1", "gamertag"),
            ("ps4", "psn"),
            ("ps3", "psn"),
        ):
            with self.subTest(platform=platform):
                response = self.client.get(reverse("api_" + platform + "_list"))
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.data), 1)
                self.assertEqual(response.data[0]["level"], 50)
                self.assertIn(account_field, response.data[0])
                self.assertNotIn("created_by", response.data[0])

    def test_openapi_schema_still_loads(self):
        response = self.client.get(reverse("openapi-schema"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["openapi"].startswith("3."))
