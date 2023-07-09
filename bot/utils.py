# By < @xditya >
# // @BotzHub //

import sys
import logging
import importlib
from pathlib import Path

def load_plugins(plugin_name):
    path = Path(f"bot/plugins/{plugin_name}.py")
    name = "bot.plugins.{}".format(plugin_name)
    spec = importlib.util.spec_from_file_location(name, path)
    load = importlib.util.module_from_spec(spec)
    load.logger = logging.getLogger(plugin_name)
    spec.loader.exec_module(load)
    sys.modules["bot.plugins." + plugin_name] = load
    print("Bot has Imported " + plugin_name)


"----------------------------------------------------------------------------------------------"


def get_readable_time(seconds: int) -> str:
    count = 0
    readable_time = ""
    time_list = []
    time_suffix_list = [" seconds", "m", "h", " days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        readable_time += f"{time_list.pop()}, "

    time_list.reverse()
    readable_time += " ".join(time_list)

    return readable_time


"--------------------------------------------------------------------------------------"


async def get_userid_by_name(username):
    try:
        return (REDIS.hget('user', username))
    except:
        return None


async def get_user_id(username):
    # ensure valid userid
    if len(username) <= 5:
        return None

    if username.startswith("@"):
        username = username[1:]

    users = await get_userid_by_name(username)

    if not users:
        return None

    elif len(users) == 1:
        return users[0].user_id

    else:
        for user_obj in users:
            try:
                userdat = await telethn.get_entity(user_obj.user_id)
                if userdat.username == username:
                    return userdat.id
            except:
                LOGGER.info("Error extracting user id.")

    return None