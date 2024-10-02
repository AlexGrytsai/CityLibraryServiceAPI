from decimal import Decimal

import stripe
from django.conf import settings
from stripe.checkout import Session

from borrowing.models import Borrowing
from payment.models import PaymentModel


class PaymentManager:
    FINE_MULTIPLIER = 2

    def __init__(self, borrowing: Borrowing) -> None:
        stripe.api_key = settings.STRIPE_SECRET_KEY

    @staticmethod
    def __calculate_money_to_pay_cents(days: int, daily_fee: Decimal) -> int:
        return int(days * daily_fee * 100)

    @staticmethod
    def __create_stripe_session(
        borrowing: Borrowing,
        unit_amount: int,
        describe_payment: str = "Payment for borrowing of book",
    ) -> Session:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": unit_amount,
                        "product_data": {
                            "name": f"Borrowing of {borrowing.book.title} "
                                    f"(Borrowing ID: {borrowing.id})",
                            "description": describe_payment,
                        },
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=settings.STRIPE_SUCCESS_URL,
            cancel_url=settings.STRIPE_CANCEL_URL,
        )
        return session

    def create_payment(self, borrowing: Borrowing) -> None:
        days_borrowed = (
            borrowing.expected_return_date - borrowing.borrow_date
        ).days
        daily_fee = borrowing.book.daily_fee
        unit_amount = self.__calculate_money_to_pay_cents(
            days_borrowed, daily_fee
        )

        stripe_session = self.__create_stripe_session(borrowing, unit_amount)

        PaymentModel.objects.create(
            borrow=borrowing,
            session_url=stripe_session.url,
            session_id=stripe_session.id,
            money_to_pay=unit_amount,
            type=PaymentModel.Type.PAYMENT,
        )

    def create_fine_payment(self, borrowing: Borrowing) -> None:
        days_fine = (
            borrowing.actual_return_date - borrowing.expected_return_date
        ).days
        daily_fee = borrowing.book.daily_fee

        unit_amount = self.__calculate_money_to_pay_cents(
            days_fine, daily_fee
        ) * self.FINE_MULTIPLIER

        stripe_session = self.__create_stripe_session(
            borrowing,
            unit_amount,
            describe_payment="Fine payment for borrowing of book"
        )

        PaymentModel.objects.create(
            borrow=borrowing,
            session_url=stripe_session.url,
            session_id=stripe_session.id,
            money_to_pay=unit_amount,
            type=PaymentModel.Type.FINE,
        )
