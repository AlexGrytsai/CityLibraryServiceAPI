import asyncio
import logging
from datetime import timedelta

from celery import shared_task
from dateutil.utils import today
from dotenv import load_dotenv

from borrowing.models import Borrowing
from notification.telegram import TelegramNotification

load_dotenv()

logger = logging.getLogger("my_debug")


@shared_task
def notify_new_borrowing(borrowing_details: str) -> None:
    message = f"New Borrowing: {borrowing_details}"

    logger.info("Start sending message to staff users")
    asyncio.run(
        TelegramNotification().send_telegram_message_to_staff_users(message)
    )


@shared_task
def notify_overdue_borrowings() -> None:
    tomorrow_date = today() + timedelta(days=1)
    overdue_borrowings = Borrowing.objects.filter(
        actual_return_date=None, expected_return_date__lt=tomorrow_date
    )
    if not overdue_borrowings:
        message = "No borrowings overdue today!"
        asyncio.run(
            TelegramNotification().send_telegram_message_to_staff_users(
                message
            )
        )
    else:
        for borrowing in overdue_borrowings:
            message = (
                f"Overdue Borrowing Alert!\n"
                f"User: {borrowing.user.email}\n"
                f"Book: {borrowing.book.title}\n"
                f"Expected Return Date: {borrowing.expected_return_date}\n"
            )
            asyncio.run(
                TelegramNotification().send_telegram_message_to_staff_users(
                    message
                )
            )


@shared_task
def notify_successfully_payed(message: str) -> None:
    asyncio.run(
        TelegramNotification().send_telegram_message_to_staff_users(
            message
        )
    )
