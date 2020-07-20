from django.test import TestCase
from pawnlisting.models import Pawn
from django.shortcuts import reverse

from pawnlisting.tests.utility import UtilityTestCase

class TestPawnApi(UtilityTestCase):

    def test_pawn_list_api(self):
        response = self.client.get(reverse("api_pawn_list"))
        self.assertEqual(response.status_code, 200)
        pawn_api_data = {k: v for k, v in response.data[0].items()}

        user = self.create_args[0]
        name = self.create_args[1]
        platform = self.create_args[2]
        pawn_data, profile_data = self.generate_pawn_data(name=name, platform=platform, created_by=user)
        
        for k, v in pawn_data.items():
            if k == "created_by":
                v = v.id
            self.assertEqual(v, pawn_api_data[k])