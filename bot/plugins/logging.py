from telethon import events
from bot import REDIS, telethn, LOGGER

@telethn.on(events.NewMessage)
async def handle_new_message(event):
    if not event.from_id:
        return
    # Save user in Redis
    user_id = event.sender_id
    user_name = event.sender.username  
    if REDIS.hget('user', user_name) == user_id:
        return
    REDIS.hset('user', user_name, user_id)
