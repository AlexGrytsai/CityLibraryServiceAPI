from django.db import IntegrityError
from django.test import TestCase

from books.models import Book


class BookModelTest(TestCase):

    def test_book_string_representation(self):
        book = Book.objects.create(
            title="Test Book",
            author="John Doe",
            cover=Book.Cover.HARD,
            inventory=10,
            daily_fee=5.99,
        )
        self.assertEqual(str(book), "Test Book by John Doe")

    def test_book_ordering(self):
        book1 = Book.objects.create(
            title="A Test Book",
            author="John Doe",
            cover=Book.Cover.HARD,
            inventory=10,
            daily_fee=5.99,
        )
        book2 = Book.objects.create(
            title="B Test Book",
            author="Jane Doe",
            cover=Book.Cover.SOFT,
            inventory=5,
            daily_fee=4.99,
        )
        books = Book.objects.all()
        self.assertEqual(books[0], book1)
        self.assertEqual(books[1], book2)

    def test_book_unique_constraint(self):
        Book.objects.create(
            title="Test Book",
            author="John Doe",
            cover=Book.Cover.HARD,
            inventory=10,
            daily_fee=5.99,
        )
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                title="Test Book",
                author="John Doe",
                cover=Book.Cover.SOFT,
                inventory=5,
                daily_fee=4.99,
            )

    def test_book_check_constraint_inventory(self):
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                title="Test Book",
                author="John Doe",
                cover=Book.Cover.HARD,
                inventory=-1,
                daily_fee=5.99,
            )

    def test_book_check_constraint_daily_fee(self):
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                title="Test Book",
                author="John Doe",
                cover=Book.Cover.HARD,
                inventory=10,
                daily_fee=-5.99,
            )
