from django.db import models

from borrowing.models import Borrowing


class PaymentModel(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"

    class Type(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINE = "FINE", "Fine"

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    type = models.CharField(max_length=10, choices=Type.choices, default=Type.PAYMENT)
    borrow = models.ForeignKey(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["-id"]