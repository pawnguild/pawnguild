from django.test import TestCase
from pawnlisting.models import Pawn
from django.shortcuts import reverse

from crum import get_current_user, impersonate

from pawnlisting.tests.utility import Utility

class TestPawnApi(Utility, TestCase):

    def setUp(self):
        user = self.create_user_log_in("testuser")
        self.pawn_data = self.generate_pawn_data(name="T1")
        with impersonate(user):
            self.created_pawn = Pawn.objects.create(**self.pawn_data)


    def test_pawn_list_api(self):
        response = self.client.get(reverse("api_pawn_list"))
        self.assertEqual(response.status_code, 200)
    
        pawn_api_data = {k: v for k, v in response.data[0].items()}
        for k, v in self.pawn_data.items():
            self.assertEqual(v, pawn_api_data[k])