from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user, get_user_model

from time import sleep
from datetime import datetime, timedelta

from pawnguild.pawnlisting.tests.utility import UtilityTestCase


class EmailBackendTests(UtilityTestCase):

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_bad_email_fails(self):
        with self.assertRaises(get_user_model().DoesNotExist):
            self.client.login(username=self.user.email + "not_a_real_email", password="12345")


    def test_login_with_email(self):
        self.client.login(username=self.user.email, password="12345")
        self.assertTrue(get_user(self.client).is_authenticated)        


