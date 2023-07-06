from bot import pgram, telethn
from pyrogram import filters
from telethon import events


@pgram.on_message(filters.command("alive"))
async def pyrocheck(_, message):
    await message.reply("Pyrogram client is alive.")


@telethn.on(events.NewMessage(incoming=True, pattern="/alivet"))
async def tstart(event):
    await event.reply("Telethon client is alive.")