from rest_framework import serializers

from borrowing.models import Borrowing
from payment.models import PaymentModel


class PaymentListSerializer(serializers.ModelSerializer):
    borrow = serializers.SerializerMethodField()
    class Meta:
        model = PaymentModel
        fields = [
            "id",
            "status",
            "borrow",
            "money_to_pay",
        ]

    def get_borrow(self, obj: PaymentModel):
        return f"Borrowing ID: {obj.borrow.id}. Book: {obj.borrow.book.title}"

class PaymentDetailSerializer(PaymentListSerializer):
    class Meta(PaymentListSerializer.Meta):
        fields = PaymentListSerializer.Meta.fields + [
            "type", "session_url", "session_id"
        ]