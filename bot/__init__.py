from pyrogram import Client
import logging
from os import getenv

from dotenv import load_dotenv
from telethon import TelegramClient

from redis import StrictRedis


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()], level=logging.INFO)

LOGGER = logging.getLogger(__name__)


load_dotenv()

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_NAME = getenv("BOT_NAME")
SUPPORT_CHAT = getenv("SUPPORT_CHAT")
TOKEN = getenv("TOKEN")
REDIS_URL = getenv("REDIS_URL")


pgram = Client("pgram", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN, sleep_threshold=0)
telethn = TelegramClient("telethn", API_ID, API_HASH).start(bot_token=TOKEN)


REDIS = StrictRedis.from_url(REDIS_URL, decode_responses=True)

try:
    REDIS.ping()
    LOGGER.info("Your redis server is now alive!")

except BaseException:
    raise Exception("Your redis server is not alive, please check again.")

finally:
    REDIS.ping()
    LOGGER.info("Your redis server is now alive!")