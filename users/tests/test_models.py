from django.contrib.auth import get_user_model
from django.test import TestCase


class TestUserModel(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_user_creation(self):
        user = self.User.objects.create_user(
            email="test@example.com", password="password"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, None)

    def test_user_str_representation(self):
        user = self.User.objects.create_user(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            password="password",
        )
        self.assertEqual(str(user), "John Doe")

    def test_user_str_representation_with_username(self):
        user = self.User.objects.create_user(
            email="test@example.com", username="testuser", password="password"
        )
        self.assertEqual(str(user), "testuser")

    def test_user_str_representation_with_empty_fields(self):
        user = self.User.objects.create_user(
            email="test@example.com", password="password"
        )
        self.assertEqual(str(user), "test@example.com")
