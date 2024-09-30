from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from books.serializers import BookSerializer, BookListSerializer
from books.views import BookViewSet


class BookViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_user(
            email="admin@example.com", password="testpassword", is_staff=True
        )
        self.user = get_user_model().objects.create_user(
            email="test@example",
            password="testpassword",
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="John Doe",
            cover=Book.Cover.HARD,
            inventory=10,
            daily_fee=5.99,
        )

    def test_get_book_list(self):
        response = self.client.get(reverse("books:book-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Test Book")

    def test_get_book_detail(self):
        response = self.client.get(
            reverse("books:book-detail", kwargs={"pk": self.book.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("books:book-detail", kwargs={"pk": self.book.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Book")

        self.client.force_authenticate(user=self.admin)
        response = self.client.get(
            reverse("books:book-detail", kwargs={"pk": self.book.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Book")

    def test_post_book(self):
        data = {
            "title": "New Book",
            "author": "Jane Doe",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 5.99,
        }
        response = self.client.post(
            reverse("books:book-list"), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse("books:book-list"), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            reverse("books:book-list"), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_book(self):
        data = {
            "title": "Updated Book",
            "author": "John Doe",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 5.98,
        }
        response = self.client.put(
            reverse("books:book-detail", kwargs={"pk": self.book.pk}),
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            reverse("books:book-detail", kwargs={"pk": self.book.pk}),
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin)
        response = self.client.put(
            reverse("books:book-detail", kwargs={"pk": self.book.pk}),
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        response = self.client.delete(
            reverse("books:book-detail", kwargs={"pk": self.book.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse("books:book-detail", kwargs={"pk": self.book.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(
            reverse("books:book-detail", kwargs={"pk": self.book.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_serializer_class(self):
        view = BookViewSet()
        view.action = None
        self.assertEqual(view.get_serializer_class(), BookSerializer)
        view.action = "list"
        self.assertEqual(view.get_serializer_class(), BookListSerializer)
