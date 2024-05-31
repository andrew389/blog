import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from telegram.ext import Application
from telegram import BotCommand
from env_config.config import FILE_PATH, BOT_TOKEN


async def notify_new_article(article):
    with open(FILE_PATH, "r") as file:
        chat_ids = file.readlines()

    for chat_id in chat_ids:
        chat_id = chat_id.strip()
        if chat_id:
            bot = Application.builder().token(BOT_TOKEN).build().bot
            message = f"New Article:\n\nTitle: {article['title']}\n\nBody: {article['body']}"
            await bot.send_message(chat_id=chat_id, text=message)


async def set_commands(application: Application) -> None:
    commands = [
        BotCommand("start", "Welcome message"),
        BotCommand("help", "List of available commands"),
        BotCommand("latest", "Get the latest article"),
        BotCommand("subscribe", "Subscribe to new article notifications"),
        BotCommand("unsubscribe", "Unsubscribe from new article notifications"),
    ]
    await application.bot.set_my_commands(commands)
