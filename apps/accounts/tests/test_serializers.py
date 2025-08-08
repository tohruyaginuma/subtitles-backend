from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.serializers import RegisterSerializer  
from accounts.serializers import LoginSerializer  # Adjust if needed

User = get_user_model()

class RegisterSerializerTest(TestCase):
    def test_serializer_valid_data_creates_user(self):
        data = {
            "email": "user@example.com",
            "password": "securepass123"
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        user = serializer.save()
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))
        self.assertTrue(User.objects.filter(email="user@example.com").exists())

    def test_serializer_missing_email(self):
        data = {
            "password": "securepass123"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_serializer_missing_password(self):
        data = {
            "email": "user@example.com"
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)

    def test_password_is_write_only(self):
        serializer = RegisterSerializer()
        self.assertTrue(serializer.fields["password"].write_only)

class LoginSerializerTest(TestCase):
    def setUp(self):
        self.email = "user@example.com"
        self.password = "strongpass123"
        self.user = User.objects.create_user(email=self.email, password=self.password)

    def test_valid_credentials(self):
        data = {
            "email": self.email,
            "password": self.password
        }
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["user"], self.user)

    def test_invalid_password(self):
        data = {
            "email": self.email,
            "password": "wrongpassword"
        }
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(serializer.errors["non_field_errors"][0], "Invalid email or password")

    def test_nonexistent_user(self):
        data = {
            "email": "notfound@example.com",
            "password": "any"
        }
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_missing_fields(self):
        serializer = LoginSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.assertIn("password", serializer.errors)