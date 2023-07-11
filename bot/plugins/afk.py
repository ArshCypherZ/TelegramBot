"""
MIT License

Copyright (c) 2022 Arsh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import time

from bot import REDIS, telethn, LOGGER
from bot.utils import get_readable_time, get_user_id
from bot.database.afk_redis import afk_reason, end_afk, is_user_afk, start_afk

from telethon import events
from telethon.tl.types import MessageEntityMention, MessageEntityMentionName, MessageEntityBotCommand

AFK_GROUP = 7
AFK_REPLY_GROUP = 8


@telethn.on(events.NewMessage(incoming=True, pattern="/afk"))
async def afk(event):
    args = event.text.split(None, 1)
    if not event.from_id:  # ignore channels
        return
    start_afk_time = time.time()
    reason = args[1] if len(args) >= 2 else "none"
    start_afk(event.sender_id, reason)
    REDIS.set(f"afk_time_{event.sender_id}", start_afk_time)
    fname = event.sender.first_name
    await event.reply(f"{fname} is now away!")


@telethn.on(events.NewMessage)
async def no_longer_afk(event):
    if not event.from_id:  # ignore channels
        return
    
    for ent, text in event.get_entities_text():
        cum, gae = None, None
        if isinstance(ent, MessageEntityBotCommand):
            return

    if not (is_user_afk(event.sender_id)):  # Check if user is afk or not
        return
    end_afk_time = get_readable_time(
        (time.time() - float(REDIS.get(f"afk_time_{event.sender_id}")))
    )
    REDIS.delete(f"afk_time_{event.sender_id}")
    if res := end_afk(event.sender_id):
        firstname = event.sender.first_name
        await event.reply(f"{firstname} is back online!\n\nYou were gone for {end_afk_time}.")


@telethn.on(events.NewMessage)
async def reply_afk(event):
    userc_id = event.sender_id
    if event.entities:
        for ent, text in event.get_entities_text():
            cum, gae = None, None
            if isinstance(ent, MessageEntityMentionName):
                users = ent.user_id
                LOGGER.info(users)
            elif isinstance(ent, MessageEntityMention):
                LOGGER.info(text)
                users = await get_user_id(text)
                LOGGER.info(users)
            else:
                users = None
            
        if users:
            gae = await telethn.get_entity(int(users))
            LOGGER.info(gae)
            fst_name = gae.first_name 
            await check_afk(event, users, fst_name, userc_id)
        else:
            return

    elif event.reply_to_msg_id:
        r = await event.get_reply_message()
        if not r.from_id:
            return
        user_id = r.sender_id
        fst_name = r.sender.first_name
        await check_afk(event, user_id, fst_name, userc_id)


async def check_afk(event, user_id, fst_name, userc_id):
    if (is_user_afk(user_id)):
        reason = afk_reason(user_id)
        since_afk = get_readable_time(
            (time.time() - float(REDIS.get(f"afk_time_{user_id}")))
        )
        if int(userc_id) == int(user_id):
            return
        if reason == "none":
            res = f"{fst_name} is afk.\n\nLast seen {since_afk} ago."
        else:
            res = f"{fst_name} is afk.\nReason: {reason}\n\nLast seen {since_afk} ago."

        await event.reply(res)
