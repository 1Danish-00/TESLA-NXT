# For The-TG-Bot v3
# By Priyam Kalra

import os
from asyncio import sleep
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors.rpcerrorlist import UserAlreadyParticipantError, FloodWaitError
from telethon.errors import ChannelPrivateError
from userbot.events import register
from userbot import CMD_HELP, STORAGE, LOGS, UNLOCKED_CHATS, bot

if not hasattr(STORAGE, "MESSAGE_REPO"):
    STORAGE.MESSAGE_REPO = False


async def authorize(event):
	try:
		chat = await event.get_chat()
		tag = f"@{chat.username}"
		if tag in UNLOCKED_CHATS:
			if event.sticker:
				return True
			elif event.gif:
				return True
	except:
		pass
	return False


@register(outgoing=True, func=authorize)
async def sticker_unlock(event):
    chat="@StickersBypass69"
    reply=await event.get_reply_message()
    media_repr="GIF" if event.gif else "Sticker"
    media=event.message
    if not STORAGE.MESSAGE_REPO:
        try:
            await client(JoinChannelRequest(channel=chat))
        except ChannelPrivateError:
            return await event.edit(f"Chat not found!")
        except FloodWaitError as e:
            return await event.reply(f"Too many requests, try again after {e.seconds} seconds.")
        finally:
            STORAGE.MESSAGE_REPO=True
    try:
        message=await client.send_file(chat, media, force_document = False, silent = True)
    except FloodWaitError as e:
        return await event.reply(f"Too many requests, try again after {e.seconds} seconds.")
    await bot.send_message(event.chat_id, f"[{media_repr}](t.me/{chat[1:]}/{message.id})", reply_to = reply, link_preview = True)
    await event.delete()
    await sleep(2)
    await message.delete()

# Keep the chat clean
@register(incoming = True, func = lambda e: e.chat_id == -1001247630906)
async def clean_chat(e):
    if e.sticker or e.gif:
        await sleep(2)
    await e.delete()

CMD.HELP.update({
    "unlocker": "\
Usage: Worksaround bot \"admin-only\" locks in chats.\
\nNote: This will only work if links arent filtred.\
\nWhat can be sent in chats where its locked (for now):\
\n- Stickers\
\n- GIFS\
\n\nYou need to add a chat to `UNLOCKED_CHATS` enviroment variable for this to take effect in those chats.\
"
})
