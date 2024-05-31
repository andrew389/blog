import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import logging
import requests
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
from env_config.config import FILE_PATH, DJANGO_API_URL

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext) -> None:
    """
    Handle the /start command by sending a welcome message and adding the user to the subscription list.

    Args:
        update (Update): The incoming update from Telegram.
        context (CallbackContext): The context for the callback.
    """
    keyboard = [
        [
            KeyboardButton("/start"), KeyboardButton("/help"), KeyboardButton("/latest"),
        ],
        [
            KeyboardButton("/subscribe"), KeyboardButton("/unsubscribe")
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text('Welcome to the Blog Bot!', reply_markup=reply_markup)

    chat_id = update.message.chat_id
    context.user_data['chat_id'] = chat_id

    with open(FILE_PATH, "a") as file:
        file.write(f"{chat_id}\n")


async def help_command(update: Update, context: CallbackContext) -> None:
    """
    Handle the /help command by sending a list of available commands.

    Args:
        update (Update): The incoming update from Telegram.
        context (CallbackContext): The context for the callback.
    """
    await update.message.reply_text('/start - Welcome message\n'
                                    '/help - List of available commands\n'
                                    '/latest - Get the latest article\n'
                                    '/subscribe - Subscribe to new article notifications\n'
                                    '/unsubscribe - Unsubscribe from new article notifications')


async def latest(update: Update, context: CallbackContext) -> None:
    """
    Handle the /latest command by fetching and sending the latest article from the Django API.

    Args:
        update (Update): The incoming update from Telegram.
        context (CallbackContext): The context for the callback.
    """
    response = requests.get(DJANGO_API_URL)

    if response.status_code == 200:
        articles = response.json()
        if articles:
            latest_article = articles[-1]
            await update.message.reply_text(
                f"Latest Article:\n\nTitle: {latest_article['title']}\n\nBody: {latest_article['body']}")
        else:
            await update.message.reply_text('No articles found.')
    else:
        await update.message.reply_text('Failed to fetch the latest article.')


async def subscribe(update: Update, context: CallbackContext) -> None:
    """
    Handle the /subscribe command by adding the user to the subscription list.

    Args:
        update (Update): The incoming update from Telegram.
        context (CallbackContext): The context for the callback.
    """
    chat_id = update.message.chat_id

    with open(FILE_PATH, "r") as file:
        chat_ids = file.read().splitlines()

    if str(chat_id) not in chat_ids:
        with open(FILE_PATH, "a") as file:
            file.write(f"{chat_id}\n")
        await update.message.reply_text('You have subscribed to new article notifications.')
    else:
        await update.message.reply_text('You are already subscribed.')


async def unsubscribe(update: Update, context: CallbackContext) -> None:
    """
    Handle the /unsubscribe command by removing the user from the subscription list.

    Args:
        update (Update): The incoming update from Telegram.
        context (CallbackContext): The context for the callback.
    """
    chat_id = update.message.chat_id

    with open(FILE_PATH, "r") as file:
        chat_ids = file.read().splitlines()

    with open(FILE_PATH, "w") as file:
        for id_ in chat_ids:
            if id_ != str(chat_id):
                file.write(f"{id_}\n")
    await update.message.reply_text('You have unsubscribed from new article notifications.')
