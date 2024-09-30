import logging
from datetime import date, timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from books.models import Book
from borrowing.models import Borrowing


class TestBorrowingModel(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="password"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="John Doe",
            cover=Book.Cover.HARD,
            inventory=10,
            daily_fee=5.99,
        )
        logger = logging.getLogger("django")
        logger.handlers = [h for h in logger.handlers if h.name != "redis"]

    @patch("borrowing.serializers.notify_new_borrowing")
    def test_borrowing_str_representation(self, mock_notify_new_borrowing):
        future_date = date.today() + timedelta(days=7)
        borrowing = Borrowing.objects.create(
            user=self.user, book=self.book, expected_return_date=future_date
        )
        self.assertEqual(
            str(borrowing), "Test Book borrowed by test@example.com"
        )

    def test_borrowing_creation_fails_with_invalid_dates(self):
        with self.assertRaises(IntegrityError):
            Borrowing.objects.create(
                user=self.user,
                book=self.book,
                expected_return_date="2022-12-31",
            )

    def test_borrowing_creation_fails_with_non_unique_combination(self):
        future_date = date.today() + timedelta(days=7)

        Borrowing.objects.create(
            user=self.user, book=self.book, expected_return_date=future_date
        )
        with self.assertRaises(IntegrityError):
            Borrowing.objects.create(
                user=self.user,
                book=self.book,
                expected_return_date=future_date,
            )

    def test_borrowing_save_fails_when_modifying_actual_return_date(self):
        future_date = date.today() + timedelta(days=7)
        borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date=future_date,
            actual_return_date="2023-12-25",
        )
        borrowing.actual_return_date = "2023-12-26"
        with self.assertRaises(ValidationError):
            borrowing.save()
