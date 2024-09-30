import logging
import os

from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

logger = logging.getLogger("my_debug")


class TelegramNotification:
    def __init__(self) -> None:
        telegram_token = os.getenv("TELEGRAM_TOKEN")
        if not telegram_token:
            logger.error("TELEGRAM_TOKEN is not set")
            raise ValueError("TELEGRAM_TOKEN is not set in the environment")

        try:
            self.bot = Bot(token=telegram_token)
        except Exception as e:
            logger.error(f"Telegram bot error: {e}")
            raise

    @staticmethod
    def __get_staff_users_chat_ids_list() -> list[int]:
        staff_users_chat_ids = os.getenv("STAFFUSERS_CHAT_IDS").split(",")
        if staff_users_chat_ids:
            list_chat_ids = [
                int(chat_id) for chat_id in staff_users_chat_ids if
                chat_id.strip()
            ]
            logger.info(f"Staff users chat ids: {list_chat_ids}")
            return list_chat_ids
        logger.info("Staff users chat ids: []")
        return []

    async def send_telegram_message_to_staff_users(self, text: str) -> None:
        staff_users = self.__get_staff_users_chat_ids_list()
        for chat_id in staff_users:
            logger.info(f"Send message to chat id: {chat_id}")
            await self.bot.send_message(chat_id=chat_id, text=text)
