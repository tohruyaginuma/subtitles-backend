from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.serializers import RegisterSerializer  
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# Create your tests here.
class RegisterViewTest(APITestCase):
    def setUp(self):
        # Use the URL name for your RegisterView route
        self.url = reverse('register')  # adjust this if your URL name is different

    def test_successful_registration(self):
        data = {
            "email": "newuser@example.com",
            "password": "strongpassword123"
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("data", response.data)
        self.assertIn("user_id", response.data["data"])
        self.assertIsNone(response.data["error"])

    def test_validation_error(self):
        data = {
            "username": "",  # Invalid: required
            "email": "not-an-email",  # Invalid format
            "password": "123"  # Weak password depending on your serializer
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertIsInstance(response.data["error"], dict)

    def test_general_exception(self):
        # You can simulate a crash using mock, or trigger a known failure.
        from unittest.mock import patch

        with patch('accounts.serializers.RegisterSerializer.is_valid', side_effect=Exception("Unexpected failure")):
            data = {
                "username": "anotheruser",
                "email": "test@example.com",
                "password": "password123"
            }
            response = self.client.post(self.url, data, format='json')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("error", response.data)
            self.assertEqual(response.data["error"], "Unexpected failure")

class LoginViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("login")  # make sure your urls.py has name='login'
        self.email = "loginuser@example.com"
        self.password = "securepassword123"
        self.user = User.objects.create_user(email=self.email, password=self.password)

    def test_successful_login(self):
        data = {
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(self.url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertIn("access", response.data["data"])
        self.assertIn("refresh", response.data["data"])
        self.assertIsNone(response.data["error"])

    def test_login_invalid_password(self):
        data = {
            "email": self.email,
            "password": "wrongpassword"
        }
        response = self.client.post(self.url, data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(response.data["data"])
        self.assertIn("error", response.data)

    def test_login_invalid_email(self):
        data = {
            "email": "nonexistent@example.com",
            "password": "any"
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(response.data["data"])
        self.assertIn("error", response.data)

    def test_login_missing_fields(self):
        data = {}  # no email or password
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNone(response.data["data"])
        self.assertIn("error", response.data)

    def test_login_raises_unexpected_exception(self):
        from unittest.mock import patch

        with patch("accounts.serializers.LoginSerializer.is_valid", side_effect=Exception("Unexpected error")):
            data = {
                "email": self.email,
                "password": self.password
            }
            response = self.client.post(self.url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIsNone(response.data["data"])
            self.assertEqual(response.data["error"], "Unexpected error")