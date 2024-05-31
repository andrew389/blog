import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import asyncio
from telegram.ext import Application, CommandHandler
from handlers import start, help_command, latest, subscribe, unsubscribe
from notifications import set_commands
from env_config.config import BOT_TOKEN


def main() -> None:
    """
    Start the bot and set up event handlers.
    """
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("latest", latest))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_commands(application))

    application.run_polling()


if __name__ == '__main__':
    main()