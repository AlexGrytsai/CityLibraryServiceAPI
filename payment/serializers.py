from rest_framework import serializers

from payment.models import PaymentModel


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentModel
        fields = [
            "status",
            "type",
            "borrow",
            "session_url",
            "session_id",
            "money_to_pay",
        ]
