import logging

from django.db.models import Q
from rest_framework import serializers

from books.models import Book
from borrowing.models import Borrowing

logger = logging.getLogger("my_debug")


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all().filter(Q(inventory__gt=0))
    )

    class Meta:
        model = Borrowing
        fields = [
            "expected_return_date",
            "book",
        ]

    def create(self, validated_data: dict) -> Borrowing:
        logger.info(f"User borrowed book '{validated_data['book']}'")

        return Borrowing.objects.create(**validated_data)


class BorrowingListSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        ]

    def get_book(self, obj: Borrowing) -> str:
        return obj.book.title
