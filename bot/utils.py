# By < @xditya >
# // @BotzHub //

import sys
import logging
import importlib
from pathlib import Path

from typing import List

from pyrogram import Client, errors, raw

from bot import REDIS, LOGGER, telethn

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
    return (REDIS.hget('user', username))



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

"---------------------------------------------------------------------------------"


# thanks to hamkercat
async def get_sticker_set_by_name(
    client: Client, name: str
) -> raw.base.messages.StickerSet:
    try:
        return await client.invoke(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetShortName(short_name=name),
                hash=0,
            )
        )
    except errors.exceptions.not_acceptable_406.StickersetInvalid:
        return None


# Known errors: (I don't see a reason to catch them as we, for sure, won't face them right now):
# errors.exceptions.bad_request_400.PackShortNameInvalid -> pack name needs to end with _by_botname
# errors.exceptions.bad_request_400.ShortnameOccupyFailed -> pack's name is already in use


async def create_sticker_set(
    client: Client,
    owner: int,
    title: str,
    short_name: str,
    stickers: List[raw.base.InputStickerSetItem],
) -> raw.base.messages.StickerSet:
    return await client.invoke(
        raw.functions.stickers.CreateStickerSet(
            user_id=await client.resolve_peer(owner),
            title=title,
            short_name=short_name,
            stickers=stickers,
        )
    )


async def add_sticker_to_set(
    client: Client,
    stickerset: raw.base.messages.StickerSet,
    sticker: raw.base.InputStickerSetItem,
) -> raw.base.messages.StickerSet:
    return await client.invoke(
        raw.functions.stickers.AddStickerToSet(
            stickerset=raw.types.InputStickerSetShortName(
                short_name=stickerset.set.short_name
            ),
            sticker=sticker,
        )
    )


async def create_sticker(
    sticker: raw.base.InputDocument, emoji: str
) -> raw.base.InputStickerSetItem:
    return raw.types.InputStickerSetItem(document=sticker, emoji=emoji)