from django.test import TestCase
from pawnlisting.models import Pawn
from django.shortcuts import reverse

from pawnlisting.tests.utility import UtilityTestCase

class TestPawnApi(UtilityTestCase):

    def test_pawn_list_api(self):
        response = self.client.get(reverse("api_pawn_list"))
        self.assertEqual(response.status_code, 200)
        pawn_api_data = {k: v for k, v in response.data[0].items()}
        for k, v in self.pawn_data.items():
            if k == "created_by":
                v = v.id
            self.assertEqual(v, pawn_api_data[k])