from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user

# Create your tests here.

class TestRegister(TestCase):

    def test_register(self):
        self.assertFalse(get_user(self.client).is_authenticated)        
        response = self.client.post(reverse("register"), data = {"username": "testacc",
                                                        "password1": "ventura1",
                                                        "password2": "ventura1",
                                                        "email": "foobar@gmail.com"})
        self.assertTrue(get_user(self.client).is_authenticated)        
