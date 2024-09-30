from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class UserCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_post_request(self):
        data = {
            "email": "test@example.com",
            "password": "test!23password",
        }
        response = self.client.post(reverse("users:register"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_request(self):
        response = self.client.get(reverse("users:register"))
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_put_request(self):
        response = self.client.put(reverse("users:register"))
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_delete_request(self):
        response = self.client.delete(reverse("users:register"))
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )


class ManageUserViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword"
        )

        self.client.force_authenticate(user=self.user)

    def test_get_request(self):
        response = self.client.get(reverse("users:me"))
        response.user = self.user
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_request(self):
        data = {
            "email": "test333@example.com",
        }
        response = self.client.put(reverse("users:me"), data=data)
        response.user = self.user
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            get_user_model().objects.get(id=self.user.id).email,
            "test333@example.com",
        )

    def test_patch_request(self):
        data = {
            "email": "test333@example.com",
        }
        response = self.client.patch(reverse("users:me"), data=data)
        response.user = self.user
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            get_user_model().objects.get(id=self.user.id).email,
            "test333@example.com",
        )

    def test_delete_request(self):
        response = self.client.delete(reverse("users:me"))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UserPasswordUpdateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword"
        )

        self.client.force_authenticate(user=self.user)

    def test_put_request(self):
        data = {
            "password": "new!!!32password",
        }
        response = self.client.put(reverse("users:update-password"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            get_user_model()
            .objects.get(id=self.user.id)
            .check_password("new!!!32password"),
            True,
        )
