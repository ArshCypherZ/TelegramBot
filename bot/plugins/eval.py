from bot import pgram, telethn
from telethon import events


@telethn.on(events.NewMessage(incoming=True, pattern="/eval"))
async def eval_e(event):
    if event.sender_id != 5565211830:
        return
    if len(event.text) > 5 and event.text[5] != " ":
        return
    xx = await eor(event, "`Processing..`")
    try:
        cmd = event.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await xx.delete()
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    reply_to_id = event.message.id
    try:
        await aexec(cmd, event)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = f"**OUTPUT**: \n```{cmd}``` \n"
    if len(final_output) > 4096:
        lmao = final_output.replace("`", "").replace("**", "").replace("__", "")
        with io.BytesIO(str.encode(lmao)) as out_file:
            out_file.name = "eval.txt"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=f"```{cmd}```" if len(cmd) < 998 else None,
                reply_to=reply_to_id,
            )
            await xx.delete()
    else:
        await xx.edit(final_output)


async def aexec(code, event):
    exec(
        (
            (
                ("async def __aexec(e, client): " + "\n message = event = e")
                + "\n r = await event.get_reply_message()"
            )
            + ("\n chat = (await event.get_chat()).id")
            + "\n p = print"
        )
        + "".join(f"\n {l}" for l in code.split("\n"))
    )

    return await locals()["__aexec"](event, event.client)
