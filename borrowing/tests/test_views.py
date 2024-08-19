from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)
from borrowing.views import BorrowingView


class TestBorrowingView(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = get_user_model().objects.create_user(
            email="admin@example.com", password="password", is_staff=True
        )
        self.regular_user = get_user_model().objects.create_user(
            email="user@example.com", password="password"
        )

        future_date = date.today() + timedelta(days=7)
        self.book = Book.objects.create(
            title="Test Book",
            author="John Doe",
            cover=Book.Cover.HARD,
            inventory=10,
            daily_fee=5.99,
        )
        self.borrowing1 = Borrowing.objects.create(
            user=self.admin, book=self.book, expected_return_date=future_date
        )
        self.borrowing2 = Borrowing.objects.create(
            user=self.regular_user,
            book=self.book,
            expected_return_date=future_date,
        )

    def test_retrieve_all_borrowings_for_admin(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(reverse("borrowing:borrowing-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_retrieve_borrowings_for_regular_user(self):
        self.client.force_authenticate(self.regular_user)
        response = self.client.get(reverse("borrowing:borrowing-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_borrowings_filtered_by_user_id_for_only_admin(self):
        response = self.client.get(
            reverse("borrowing:borrowing-list") + f"?user_id={self.admin.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.regular_user)
        response = self.client.get(
            reverse("borrowing:borrowing-list") + f"?user_id={self.admin.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

        self.client.force_authenticate(self.admin)
        response = self.client.get(
            reverse("borrowing:borrowing-list")
            + f"?user_id={self.regular_user.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_borrowings_filter_by_is_active_parameter(self):
        response = self.client.get(
            reverse("borrowing:borrowing-list") + f"?is_active=true"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.regular_user)
        response = self.client.get(
            reverse("borrowing:borrowing-list") + f"?is_active=true"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

        self.client.force_authenticate(self.admin)
        response = self.client.get(
            reverse("borrowing:borrowing-list") + f"?is_active=true"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

        response = self.client.get(
            reverse("borrowing:borrowing-list") + f"?is_active=false"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_get_serializer_class(self):
        view = BorrowingView()

        view.action = None
        self.assertEqual(view.get_serializer_class(), BorrowingSerializer)

        view.action = "list"
        self.assertEqual(view.get_serializer_class(), BorrowingListSerializer)

        view.action = "create"
        self.assertEqual(view.get_serializer_class(), BorrowingSerializer)

        view.action = "retrieve"
        self.assertEqual(
            view.get_serializer_class(), BorrowingDetailSerializer
        )

    def test_perform_create_success(self):
        test_book = Book.objects.create(
            title="Test Book 2",
            author="John Doe",
            cover=Book.Cover.HARD,
            inventory=2,
            daily_fee=5.99,
        )
        self.client.force_authenticate(self.regular_user)
        data = {
            "book": test_book.id,
            "expected_return_date": date.today() + timedelta(days=14),
        }

        response = self.client.post(
            reverse("borrowing:borrowing-list"), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test_book.refresh_from_db()
        self.assertEqual(test_book.inventory, 1)

    def test_perform_create_book_not_available(self):
        test_book = Book.objects.create(
            title="Test Book 2",
            author="John Doe",
            cover=Book.Cover.HARD,
            inventory=0,
            daily_fee=5.99,
        )

        self.client.force_authenticate(self.regular_user)
        data = {
            "book": test_book.id,
            "expected_return_date": date.today() + timedelta(days=14),
        }

        response = self.client.post(
            reverse("borrowing:borrowing-list"), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_book_success(self):
        self.client.force_authenticate(self.admin)
        url = reverse(
            "borrowing:borrowing-return", kwargs={"pk": self.borrowing1.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.borrowing1.refresh_from_db()
        self.assertIsNotNone(self.borrowing1.actual_return_date)
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 11)

    def test_return_book_already_returned(self):
        self.client.force_authenticate(self.admin)
        self.borrowing1.actual_return_date = date.today() - timedelta(days=1)
        self.borrowing1.save()

        url = reverse(
            "borrowing:borrowing-return", kwargs={"pk": self.borrowing1.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Book already returned")
