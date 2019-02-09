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

    def test_logout_process(self):
        """
        Note: this is NOT an IDEAL APPROACH | DONT do this
        --------------------------------------------------
        Step 1: Log user in with built-in login method of Client
        Step 2: Verify user is_authenticated property evaluates to True
        Step 3: Log user out with logout end-point
        Step 4: Verify user is_authenticated property now evaluates to False
        PS: ****> Acquire user object from self.Client to ensure changes to is properties are reflected <****

        :return:
        """
        # login user
        self.client.login(username=self.username, password=self.password)
        # Test user is authenticated
        logged_in_user = self.client.request().context['user']
        self.assertEqual(logged_in_user.is_authenticated, True)

        # Logout user
        logout_url = reverse('user:logout')
        response = self.client.get(logout_url)
        self.assertEqual(response.status_code, 302)
        # test user is Anonymous after logout
        self.assertEqual(self.client.request().context['user'].is_authenticated, False)

    def test_user_registration_landing_page(self):
        registration_url = reverse('user:register')
        response = self.client.get(registration_url)
        self.assertEqual(response.status_code, 200)

    def test_user_registration_process(self):
        register_url = reverse('user:register_do')
        # test response structure is json with expected keys
        # test empty data provided | fail
        response = self.client.post(register_url, {})
        self.assertIn('status', json.loads(response.content))
        self.assertEqual(str(response.status_code).startswith("2"), False)
        # test providing missing data: no password | fail
        response = self.client.post(register_url, {'username': get_random_string(5)})
        self.assertEqual(str(response.status_code).startswith("4"), True)
        # test providing missing data: no username | fail
        response = self.client.post(register_url, {'password': get_random_string(10)})
        self.assertEqual(str(response.status_code).startswith("4"), True)
        # Test duplicate entry
        response = self.client.post(register_url, {'username': self.username, 'password': get_random_string(16)})
        self.assertEqual(str(response.status_code).startswith("4"), True)
        # Test happy path | 201
        response = self.client.post(register_url, {'username': get_random_string(6), 'password': get_random_string(10)})
        self.assertEqual(201, response.status_code)
