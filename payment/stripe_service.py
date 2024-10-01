from decimal import Decimal

import stripe
from django.conf import settings
from stripe.checkout import Session

from borrowing.models import Borrowing
from payment.models import PaymentModel


class PaymentManager:
    def __init__(self, borrowing: Borrowing) -> None:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe_session = self.__create_stripe_session(borrowing)
        self.payment = PaymentModel.objects.create(
            borrow=borrowing,
            session_url=stripe_session.url,
            session_id=stripe_session.id,
            money_to_pay=self.__calculate_money_to_pay_usd(borrowing),
        )

    @staticmethod
    def __calculate_money_to_pay_usd(borrowing: Borrowing) -> Decimal:
        delta_days_borrowed = (
            borrowing.actual_return_date - borrowing.borrow_date
        ).days

        money_to_pay = delta_days_borrowed * borrowing.book.daily_fee

        return money_to_pay

    def __create_stripe_session(self, borrowing: Borrowing) -> Session:
        unit_amount_usd = self.__calculate_money_to_pay_usd(borrowing)
        unit_amount_cents = int(unit_amount_usd * 100)
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": unit_amount_cents,
                        "product_data": {
                            "name": f"Borrowing of {borrowing.book.title}",
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
