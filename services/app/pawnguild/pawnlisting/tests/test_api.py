from django.test import TestCase
from django.shortcuts import reverse

from pawnguild.pawnlisting.models import Pawn
from pawnguild.pawnlisting.tests.utility import UtilityTestCase


class TestPawnApi(UtilityTestCase):
    def test_pawn_list_api(self):
        return
        response = self.client.get(reverse("api_pawn_list"))
        self.assertEqual(response.status_code, 200)
        pawn_api_data = {k: v for k, v in response.data[0].items()}

        steam_pawn_data = self.generate_steam_pawn_data(
            name=self.test_args["steam_pawn_name"],
            created_by=self.test_args["test_user"],
        )

        for k, v in pawn_data.items():
            if k == "created_by":
                v = v.id
            self.assertEqual(v, pawn_api_data[k])
