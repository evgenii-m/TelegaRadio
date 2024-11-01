"""
RadioPlayerV3, Telegram Voice Chat Bot
Copyright (c) 2021  Asm Safone <https://github.com/AsmSafone>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
"""

import asyncio
from config import Config
from pyrogram.types import Message
from utils import mp, RADIO, USERNAME
from pyrogram import Client, filters, emoji

ADMINS=Config.ADMINS
CHAT_ID=Config.CHAT_ID
DEFAULT_STREAM_URL = Config.DEFAULT_STREAM_URL
msg=Config.msg

async def is_admin(_, client, message: Message):
    admins = await mp.get_admins(CHAT_ID)
    if message.from_user is None and message.sender_chat:
        return True
    if message.from_user.id in admins:
        return True
    else:
        return False

ADMINS_FILTER = filters.create(is_admin)


allcmd = ["start", "stream", "file", "stopradio", "help"]

@Client.on_message(filters.command(allcmd) & filters.group & ~filters.chat(CHAT_ID))
async def not_chat(_, m: Message):
    k=await m.reply_text("*** Sorry, You Can't Use This Bot!")
    await mp.delete(m)


@Client.on_message(filters.command(["stream"]) & ADMINS_FILTER & (filters.chat(CHAT_ID) | filters.private))
async def start_radio_by_stream_url(_, message: Message):
    if 1 in RADIO:
        k=await message.reply_text(f"{emoji.ROBOT} **Please Stop Existing Radio Stream!**")
        await mp.delete(k)
        await message.delete()
        return
    station_stream_url = message.text.split()[-1]
    await mp.start_radio_by_stream_url(station_stream_url)
    k=await message.reply_text(f"**Radio Stream Started by URL:** \n<code>{station_stream_url}</code>")
    await mp.delete(k)
    await mp.delete(message)


@Client.on_message(filters.command(["file"]) & ADMINS_FILTER & (filters.chat(CHAT_ID) | filters.private))
async def start_radio_by_file(_, message: Message):
    if 1 in RADIO:
        k=await message.reply_text(f"{emoji.ROBOT} **Please Stop Existing Radio Stream!**")
        await mp.delete(k)
        await message.delete()
        return
    if message.audio:
        audio = message.audio
        file_id = audio.file_id
        await mp.start_radio_by_file(file_id)
        k=await message.reply_text(
            f"**Radio Stream Started by file:** \n<code>{audio.title} ({audio.file_id})</code>")
        await mp.delete(k)
        await mp.delete(message)
    elif message.reply_to_message and message.reply_to_message.audio:
        audio = message.reply_to_message.audio
        file_id = audio.file_id
        await mp.start_radio_by_file(file_id)
        k=await message.reply_text(
            f"**Radio Stream Started by file:** \n<code>{audio.title} ({audio.file_id})</code>")
        await mp.delete(k)
        await mp.delete(message)
    else:
        k=await message.reply_text(f"**Audio file attachment is needed")
        await mp.delete(k)
        await mp.delete(message)



@Client.on_message(filters.command(["stopradio"]) & ADMINS_FILTER & (filters.chat(CHAT_ID) | filters.private))
async def stop_radio(_, message: Message):
    if 0 in RADIO:
        k=await message.reply_text(f"{emoji.ROBOT} **Please Start A Radio Stream First!**")
        await mp.delete(k)
        await mp.delete(message)
        return
    await mp.stop_radio()
    k=await message.reply_text(f"{emoji.CROSS_MARK_BUTTON} **Radio Stream Ended Successfully!**")
    await mp.delete(k)
    await mp.delete(message)


@Client.on_message(filters.command(["start"]) & ADMINS_FILTER & (filters.chat(CHAT_ID) | filters.private))
async def start(client, message):
    m=await message.reply_text("Bot started...")
    await mp.delete(m)
    await mp.delete(message)


@Client.on_message(filters.command(["help"]) & ADMINS_FILTER & (filters.chat(CHAT_ID) | filters.private))
async def help(client, message):
    if msg.get('help') is not None:
        await msg['help'].delete()
    msg['help'] = await message.reply_text("Help info:")
    await mp.delete(message)