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

import glob

from bing_image_downloader import downloader
from requests import get
from telethon import *
from telethon.tl.types import *

from bot import SUPPORT_CHAT, telethn


@telethn.on(events.NewMessage(incoming=True, pattern="/img"))
async def img_sampler(event):
    if event.fwd_from:
        return

    try:
        query = event.text.split(None, 1)[1]
    except IndexError:
        return await event.reply("Give something to search images for!")
    jit = f'"{query}"'
    downloader.download(
        jit,
        limit=4,
        output_dir="store",
        adult_filter_off=False,
        force_replace=False,
        timeout=60,
    )
    os.chdir(f'./store/"{query}"')
    types = ("*.png", "*.jpeg", "*.jpg")  # the tuple of file types
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(files))
    await telethn.send_file(event.chat_id, files_grabbed, reply_to=event.id)
    os.chdir("/app")
    os.system("rm -rf store")


@telethn.on(events.NewMessage(incoming=True, pattern="/google"))
async def google(event):
    if event.fwd_from:
        return
    try:
        query = event.text.split(None, 1)[1]
    except:
        return await event.reply("Give something to search on google for!")
    if " " in query:
        q = query.replace(" ", "%20")
    else:
        q = query
    wait = await event.reply("Searching on google. Please wait :3")
    gae = [Button.url("Google", f"https://www.google.com/search?q={q}")]
    meow = (f"**Search Results of {q} on Google:**").replace("%20", " ")
    try:
        req = get(f"https://api.safone.me/google?query={q}&limit=10").json() # using safone's api for google :)
        for i in range(10):
            title = req["results"][i]["title"]
            description = req["results"][i]["description"]
            link = req["results"][i]["link"]
            meow += f"\n\n• [{title}]({link})\n__{description}__"

        await event.reply(f"{meow}", buttons=gae, link_preview=False)
    except BaseException:
        await event.reply(
            f"Some error occured! Please report to @{SUPPORT_CHAT}", buttons=gae
        )
    await wait.delete()


@telethn.on(events.NewMessage(incoming=True, pattern="/ud"))
async def ud_(e):
    text = e.text.split(" ", maxsplit=1)[1]
    results = get(f"https://api.urbandictionary.com/v0/define?term={text}").json()
    try:
        reply_txt = (
            (
                f'<bold>{text}</bold>\n\n{results["list"][0]["definition"]}\n\n<i>{results["list"][0]["example"]}</i>'
            )
            .replace("[", "")
            .replace("]", "")
        )
    except BaseException:
        reply_txt = "No results found."
    await e.reply(
        reply_txt,
        buttons=Button.url("🔎 Google it!", f"https://www.google.com/search?q={text}"),
        parse_mode="html",
    )


@telethn.on(events.NewMessage(incoming=True, pattern="/define"))
async def df(event):
    try:
        input = event.text.split(None, 1)[1]
    except:
        return await event.reply("Please give some input to search the dictionary!")
    url = "https://api.dictionaryapi.dev/api/v2/entries/en/{}".format(input)
    r = get(url)
    try:
        r = r.json()[0].get("meanings")[0].get("definitions")[0].get("definition")
    except (TypeError, IndexError, KeyError):
        r = None
    if not r:
        return await event.reply("__No results found.__")
    await event.reply("**{}**:\n\n".format(input.capitalize()) + r)
