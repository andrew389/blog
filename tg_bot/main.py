import logging
import requests
import asyncio
from telegram import Update, BotCommand, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackContext
from env_config import FILE_PATH, BOT_TOKEN, DJANGO_API_URL

# Налаштування логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# Вітаюча команда
async def start(update: Update, context: CallbackContext) -> None:
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

    # Зберегти ідентифікатор чату для підписок
    chat_id = update.message.chat_id
    context.user_data['chat_id'] = chat_id
    with open(FILE_PATH, "a") as file:
        file.write(f"{chat_id}\n")


# Команда допомоги
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('/start - Welcome message\n'
                                    '/help - List of available commands\n'
                                    '/latest - Get the latest article\n'
                                    '/subscribe - Subscribe to new article notifications\n'
                                    '/unsubscribe - Unsubscribe from new article notifications')


# Команда для отримання останньої статті
async def latest(update: Update, context: CallbackContext) -> None:
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


async def notify_new_article(article):
    with open(FILE_PATH, "r") as file:
        chat_ids = file.readlines()

    for chat_id in chat_ids:
        chat_id = chat_id.strip()
        if chat_id:
            bot = Application.builder().token(BOT_TOKEN).build().bot
            message = f"New Article:\n\nTitle: {article['title']}\n\nBody: {article['body']}"
            await bot.send_message(chat_id=chat_id, text=message)


async def subscribe(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    with open(FILE_PATH, "r") as file:
        chat_ids = file.read().splitlines()
    if str(chat_id) not in chat_ids:
        with open(FILE_PATH, "a") as file:
            file.write(f"{chat_id}\n")
        await update.message.reply_text('You have subscribed to new article notifications.')
    else:
        await update.message.reply_text('You are already subscribed.')


# Команда для відписки
async def unsubscribe(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    with open(FILE_PATH, "r") as file:
        chat_ids = file.read().splitlines()
    with open(FILE_PATH, "w") as file:
        for id_ in chat_ids:
            if id_ != str(chat_id):
                file.write(f"{id_}\n")
    await update.message.reply_text('You have unsubscribed from new article notifications.')


async def set_commands(application: Application) -> None:
    commands = [
        BotCommand("start", "Welcome message"),
        BotCommand("help", "List of available commands"),
        BotCommand("latest", "Get the latest article"),
        BotCommand("subscribe", "Subscribe to new article notifications"),
        BotCommand("unsubscribe", "Unsubscribe from new article notifications"),
    ]
    await application.bot.set_my_commands(commands)


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    # Додавання обробників команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("latest", latest))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe))

    # Отримання поточного циклу подій
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_commands(application))

    # Запуск полінгу
    application.run_polling()


if __name__ == '__main__':
    main()
