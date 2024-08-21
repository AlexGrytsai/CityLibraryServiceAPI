import asyncio
import logging
import os

from celery import shared_task
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

logger = logging.getLogger("my_debug")

telegram_token = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=telegram_token)


def get_staff_users_chat_ids_list() -> list[int]:
    staff_users_chat_ids = os.getenv("STAFFUSERS_CHAT_IDS").split(",")
    if staff_users_chat_ids:
        list_chat_ids = [
            int(chat_id) for chat_id in staff_users_chat_ids if chat_id.strip()
        ]
        logger.info(f"Staff users chat ids: {list_chat_ids}")
        return list_chat_ids
    logger.info(f"Staff users chat ids: []")
    return []


async def send_telegram_message_to_staff_users(text: str) -> None:
    staff_users = get_staff_users_chat_ids_list()
    for chat_id in staff_users:
        logger.info(f"Send message to chat id: {chat_id}")
        await bot.send_message(chat_id=chat_id, text=text)


@shared_task
def notify_new_borrowing(borrowing_details: str) -> None:
    message = f"New Borrowing: {borrowing_details}"

    logger.info(f"Start sending message to staff users")
    asyncio.run(send_telegram_message_to_staff_users(message))
