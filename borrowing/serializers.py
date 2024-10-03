import logging

from django.db.models import Q
from rest_framework import serializers

from books.models import Book
from borrowing.models import BorrowingModel
from notification.tasks import notify_new_borrowing
from payment.models import PaymentModel

logger = logging.getLogger("my_debug")


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all().filter(Q(inventory__gt=0))
    )

    class Meta:
        model = BorrowingModel
        fields = [
            "expected_return_date",
            "book",
        ]

    def create(self, validated_data: dict) -> BorrowingModel:
        logger.info(f"User borrowed book '{validated_data['book']}'")

        user = validated_data["user"]
        book = validated_data["book"]
        message = (
            f"{user} (id={user.id}) borrowed book '{book}' (id={book.id})"
        )

        notify_new_borrowing(message)

        return BorrowingModel.objects.create(**validated_data)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentModel
        fields = ["id", "status", "money_to_pay"]


class BorrowingListSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    payments = PaymentSerializer(many=True, source="payment_set")

    class Meta:
        model = BorrowingModel
        fields = [
            "id",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "payments",
        ]

    def get_book(self, obj: BorrowingModel) -> str:
        return obj.book.title


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "daily_fee"]


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookDetailSerializer()
    payments = PaymentSerializer(many=True, source="payment_set")

    class Meta:
        model = BorrowingModel
        fields = [
            "id",
            "book",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "payments",
        ]
