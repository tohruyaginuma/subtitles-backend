from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class UserModelTests(TestCase):
    def test_create_user_with_email(self):
        email = 'test@example.com'
        password = 'securepass123'
        user = User.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        email = 'admin@example.com'
        password = 'adminpass123'
        user = User.objects.create_superuser(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_without_email_raises_error(self):
        with self.assertRaisesMessage(ValueError, "Email is required"):
            User.objects.create_user(email=None, password="pass")

    def test_str_method(self):
        user = User.objects.create_user(email="strtest@example.com", password="pass")
        self.assertEqual(str(user), "strtest@example.com")

    def test_update_last_login(self):
        user = User.objects.create_user(email="lastlogin@example.com", password="pass")
        self.assertIsNone(user.last_login)

        user.update_last_login()
        self.assertIsNotNone(user.last_login)

        # Allowing small delay tolerance
        self.assertAlmostEqual(user.last_login.timestamp(), timezone.now().timestamp(), delta=5)
