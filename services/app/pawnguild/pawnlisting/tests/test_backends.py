from django.contrib.auth import get_user

from pawnguild.pawnlisting.tests.utility import UtilityTestCase


class EmailBackendTests(UtilityTestCase):
    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_bad_email_fails(self):
        self.client.login(
            username=self.user.email + "not_a_real_email", password="12345"
        )
        self.assertFalse(get_user(self.client).is_authenticated)

    def test_login_with_email(self):
        self.client.login(username=self.user.email, password="12345")
        self.assertTrue(get_user(self.client).is_authenticated)
