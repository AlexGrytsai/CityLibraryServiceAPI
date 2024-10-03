from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, MagicMock

from notification.telegram import TelegramNotification


class TestTelegramNotification(IsolatedAsyncioTestCase):

    @patch(
        "notification.telegram.TelegramNotification."
        "_TelegramNotification__get_staff_users_chat_ids_list"
    )
    @patch("notification.telegram.Bot.send_message")
    async def test_send_telegram_message_to_staff_users(
        self, mock_send_message, mock_get_staff_users
    ):
        mock_get_staff_users.return_value = [12345, 67890]
        mock_send_message.return_value = MagicMock()

        telegram_notification = TelegramNotification()
        await telegram_notification.send_telegram_message_to_staff_users(
            "Test message"
        )

        self.assertEqual(mock_send_message.call_count, 2)

        mock_send_message.assert_any_call(chat_id=12345, text="Test message")
        mock_send_message.assert_any_call(chat_id=67890, text="Test message")

    @patch("os.getenv")
    def test_init_telegram_token_not_set(self, mock_getenv):
        mock_getenv.return_value = None
        with self.assertRaises(ValueError):
            TelegramNotification()

    @patch("os.getenv")
    @patch("notification.telegram.Bot")
    def test_init_telegram_token_set(self, mock_bot, mock_getenv):
        mock_getenv.return_value = "test_token"
        TelegramNotification()
        mock_bot.assert_called_once_with(token="test_token")

    @patch("os.getenv")
    def test_get_staff_users_chat_ids_list_empty(self, mock_getenv):
        mock_getenv.return_value = ""
        self.assertEqual(
            TelegramNotification.
            _TelegramNotification__get_staff_users_chat_ids_list(),
            [],
        )

    @patch("os.getenv")
    def test_get_staff_users_chat_ids_list(self, mock_getenv):
        mock_getenv.return_value = "12345,67890"
        self.assertEqual(
            TelegramNotification.
            _TelegramNotification__get_staff_users_chat_ids_list(),
            [12345, 67890],
        )
