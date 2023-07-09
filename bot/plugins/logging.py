from telethon import events
from bot import REDIS, telethn, LOGGER

@telethn.on(events.NewMessage)
async def handle_new_message(event):
    # Save user in Redis
    user_id = event.sender_id
    user_name = ""
    try:
        user_name = event.sender.username
    except:
        user_name = "None"
    REDIS.hset('user', user_id, user_name)
    LOGGER.info(f"Saved user {user_name} with ID {user_id}")