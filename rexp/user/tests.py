import unittest
from django.test import Client
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.urls import reverse
import json


class UserViewTest(unittest.TestCase):

    def setUp(self):
        self.password = get_random_string(10)
        self.username = get_random_string(5).lower()
        user = User.objects.create(
            username=self.username
        )
        user.set_password(self.password)
        user.save()
        self.user = user
        self.client = Client()

    def test_user_login_landing_page(self):
        """
        Test user login landing page
        This does not test the login process itself.
        :return:
        """
        login_url = reverse('user:login')
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, 200)

    def test_login_process(self):
        login_url = reverse('user:login_do')

        response = self.client.post(login_url, {})
        response_json = json.loads(response.content)
        # Test empty data returns error codoe not 2XX
        self.assertNotEqual(response.status_code, 200)
        # Test response is JSON
        self.assertIn('status', response_json.keys())
        # Test there is an error message
        self.assertIsNotNone(response_json['error'])
        # Test empty password fails
        response = self.client.post(login_url, {'username': self.username})
        self.assertNotEqual(response.status_code, 200)
        # Test for non-existing username
        response = self.client.post(login_url, {'username': get_random_string(6), 'password': self.password})
        self.assertNotEqual(response.status_code, 200)
        # Test wrong password
        response = self.client.post(login_url, {'username': self.username, 'password': get_random_string(13)})
        self.assertNotEqual(response.status_code, 200)
        # Test the happy path
        response = self.client.post(login_url, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)



