from bot import pgram, telethn, SUPPORT_CHAT, BOT_NAME
from uvloop import install
from pyrogram import idle
import asyncio
import glob
from pathlib import Path
from bot.utils import load_plugins


async def start():
    try:
        install()
        await pgram.start()
        await pgram.send_message(f"{SUPPORT_CHAT}", f"{BOT_NAME} has started! [PYROGRAM]")
        await idle()
        await pgram.stop()
    except Exception as e:
        LOGGER.error(e)
        LOGGER.error("Failed to send startup notification! [PYROGRAM]")

async def tstart():
    try:
        await telethn.send_message(f"{SUPPORT_CHAT}", f"{BOT_NAME} has started! [TELETHON]")
    except Exception as e:
        LOGGER.error(e)
        LOGGER.error("Failed to send startup notification! [TELETHON]")

path = "bot/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))

LOGGER.info("Bot has started!")
asyncio.get_event_loop().run_until_complete(start())
telethn.loop.run_until_complete(tstart())
telethn.run_until_disconnected()
LOGGER.info("Bot has stopped!")