import logging

from django.db.models import Q
from rest_framework import serializers

from books.models import Book
from borrowing.models import Borrowing
from users.models import User

logger = logging.getLogger("django")
class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all().filter(Q(inventory__gt=0))
    )

    class Meta:
        model = Borrowing
        fields = [
            "borrow_date",
            "expected_return_date",
            "book",
        ]

    def validate(self, data):
        if data["expected_return_date"] < data["borrow_date"]:
            user = self.context.get("request").user
            logger.error(
                f"The expected return date must be after the borrow date. "
                f"User: {user}"
            )
            raise serializers.ValidationError(
                "The expected return date must be after the borrow date"
            )
        return data
