import asyncio
import os

from celery import shared_task
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

telegram_token = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=telegram_token)


def get_staff_users_chat_ids_list() -> list[int]:
    staff_users_chat_ids = os.getenv("STAFFUSERS_CHAT_IDS").split(",")
    if staff_users_chat_ids:
        return [
            int(chat_id) for chat_id in staff_users_chat_ids if chat_id.strip()
        ]
    return []


async def send_telegram_message_to_staff_users(text: str) -> None:
    staff_users = get_staff_users_chat_ids_list()
    for chat_id in staff_users:
        await bot.send_message(chat_id=chat_id, text=text)


@shared_task
def notify_new_borrowing(borrowing_details):
    message = f"New Borrowing: {borrowing_details}"

    asyncio.run(send_telegram_message_to_staff_users(message))
