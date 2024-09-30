import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

load_dotenv()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Chat ID: {update.effective_chat.id}",
    )


if __name__ == "__main__":
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    application = ApplicationBuilder().token(telegram_token).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    application.run_polling()
