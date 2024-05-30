from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

DJANGO_API_URL = os.environ.get("DJANGO_API_URL")
DJANGO_API_SUBSCRIBE_URL = os.environ.get("DJANGO_API_SUBSCRIBE_URL")
DJANGO_API_UNSUBSCRIBE_URL = os.environ.get("DJANGO_API_UNSUBSCRIBE_URL")

FILE_PATH = os.environ.get("FILE_PATH")

SECRET_KEY = os.environ.get("SECRET_KEY")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")