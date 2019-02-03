from .models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status



class UsersTest(APITestCase):
    """Class to test user related services."""

    def setUp(self) -> None:
        """Initial set up for testing user services."""
        self.testuser = User.objects.create_user('testuser', 'testuser@test.com', 'password1234')
        self.user_register_url = reverse('user-register')
        self.user_login_url = reverse('user-login')

    def test_user_register_success(self) -> None:
        """Test that a user is able to be successfully created."""

        # valid user data
        data = {
            'username': 'testuser1',
            'email': 'testuser1@test.com',
            'password': 'password1234'
        }

        response = self.client.post(self.user_register_url, data, format='json')
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertTrue('token' in response.data)
        self.assertTrue('id' in response.data)
        self.assertFalse('password' in response.data)

    def test_user_register_fail_username_empty(self) -> None:
        """Test that user registration fails based on username being empty."""

        # username empty
        data = {
            'username': '',
            'email': 'testuser2@test.com',
            'password': 'password1234'
        }

        response = self.client.post(self.user_register_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_fail_username_short(self) -> None:
        """Test that user registration fails based on username being too short."""

        # username too short
        data = {
            'username': 'tes',
            'email': 'testuser2@test.com',
            'password': 'password1234'
        }

        response = self.client.post(self.user_register_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_fail_username_long(self) -> None:
        """Test that user registration fails based on username being too long."""

        # username too long
        data = {
            'username': 'test12345678901234567890123456789',
            'email': 'testuser2@test.com',
            'password': 'password1234'
        }

        response = self.client.post(self.user_register_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_fail_username_duplicate(self) -> None:
        """Test that user registration fails based on username being duplicate."""

        # username duplicate
        data = {
            'username': 'testuser',
            'email': 'testuser2@test.com',
            'password': 'password1234'
        }

        response = self.client.post(self.user_register_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_fail_email_empty(self) -> None:
        """Test that user registration fails based on email being empty."""

        # email empty
        data = {
            'username': 'testuser2',
            'email': '',
            'password': 'password1234'
        }

        response = self.client.post(self.user_register_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_fail_email_long(self) -> None:
        """Test that user registration fails based on email being too long."""

        # email too long
        data = {
            'username': 'testuser2',
            'email': 'testuser2123456789012345@test.com',
            'password': 'password1234'
        }

        response = self.client.post(self.user_register_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_fail_email_duplicate(self) -> None:
        """Test that user registration fails based on email being duplicate."""

        # email duplicate
        data = {
            'username': 'testuser2',
            'email': 'testuser@test.com',
            'password': 'password1234'
        }

        response = self.client.post(self.user_register_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_fail_email_invalid(self) -> None:
        """Test that user registration fails based on email being invalid."""

        # email invalid
        data = {
            'username': 'testuser2',
            'email': 'testuser2',
            'password': 'password1234'
        }

        response = self.client.post(self.user_register_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_fail_password_empty(self) -> None:
        """Test that user registration fails based on password being empty."""

        # username empty
        data = {
            'username': 'testuser2',
            'email': 'testuser2@test.com',
            'password': ''
        }

        response = self.client.post(self.user_register_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_fail_password_short(self) -> None:
        """Test that user registration fails based on password being too short."""

        # password too short
        data = {
            'username': 'testuser2',
            'email': 'testuser2@test.com',
            'password': 'passwor'
        }

        response = self.client.post(self.user_register_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_fail_password_long(self) -> None:
        """Test that user registration fails based on password being too long."""

        # password too long
        data = {
            'username': 'testuser2',
            'email': 'testuser2@test.com',
            'password': 'password1234567890123456789012345'
        }

        response = self.client.post(self.user_register_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self) -> None:
        """Test that a user is able to be successfully logged in."""

        # valid user data
        data = {
            'username': 'testuser',
            'password': 'password1234'
        }

        response = self.client.post(self.user_login_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], data['username'])
        self.assertTrue('token' in response.data)
        self.assertFalse('password' in response.data)

    def test_user_login_fail_username_empty(self) -> None:
        """Test that user login fails based on username being empty."""

        # username empty
        data = {
            'username': '',
            'password': 'password1234'
        }

        response = self.client.post(self.user_login_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_fail_username_invalid(self) -> None:
        """Test that user login fails based on username being invalid."""

        # username empty
        data = {
            'username': 'testuser2',
            'password': 'password1234'
        }

        response = self.client.post(self.user_login_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_fail_password_empty(self) -> None:
        """Test that user login fails based on password being empty."""

        # password empty
        data = {
            'username': 'testuser',
            'password': ''
        }

        response = self.client.post(self.user_login_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_fail_password_invalid(self) -> None:
        """Test that user login fails based on password being invalid."""

        # password empty
        data = {
            'username': 'testuser',
            'password': 'password12345'
        }

        response = self.client.post(self.user_login_url, data, format='json')
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
