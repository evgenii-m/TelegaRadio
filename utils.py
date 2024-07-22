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

import os
import sys
import wget
import ffmpeg
import asyncio
import subprocess
from os import path
from pyrogram import emoji
try:
    from yt_dlp import YoutubeDL
    from pytgcalls.exceptions import GroupCallNotFoundError
except ModuleNotFoundError:
    file=os.path.abspath("requirements.txt")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', file, '--upgrade'])
    os.execl(sys.executable, sys.executable, *sys.argv)
from config import Config
from asyncio import sleep
from pyrogram import Client
from signal import SIGINT
from random import randint
from pytgcalls import GroupCallFactory
from pyrogram.errors import FloodWait
from pyrogram.utils import MAX_CHANNEL_ID
from pyrogram.raw.types import InputGroupCall
from pyrogram.methods.messages.download_media import DEFAULT_DOWNLOAD_DIR
from pyrogram.raw.functions.phone import EditGroupCallTitle, CreateGroupCall


bot = Client(
    "TelegaRadioPlayerUserbot",
    Config.API_ID,
    Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)
bot.start()
e=bot.get_me()
USERNAME=e.username

from user import USER

ADMINS=Config.ADMINS
DEFAULT_STREAM_URL=Config.DEFAULT_STREAM_URL
CHAT_ID=Config.CHAT_ID
CHAT_NAME=Config.CHAT_NAME
RADIO_TITLE=Config.RADIO_TITLE
ADMIN_LIST = {}
CALL_STATUS = {}
FFMPEG_PROCESSES = {}
RADIO={6}
playlist=Config.playlist
msg=Config.msg

ydl_opts = {
    "format": "bestaudio[ext=m4a]",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)


class MusicPlayer(object):
    def __init__(self):
        self.group_call = GroupCallFactory(USER, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM).get_file_group_call()


    async def start_radio(self):
        group_call = self.group_call
        if group_call.is_connected:
            playlist.clear()   
        process = FFMPEG_PROCESSES.get(CHAT_ID)
        if process:
            try:
                process.send_signal(SIGINT)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                print(e)
                pass
            FFMPEG_PROCESSES[CHAT_ID] = ""
        station_stream_url = DEFAULT_STREAM_URL
        try:
            RADIO.remove(0)
        except:
            pass
        try:
            RADIO.add(1)
        except:
            pass
        if os.path.exists(f'radio-{CHAT_ID}.raw'):
            os.remove(f'radio-{CHAT_ID}.raw')
        # credits: https://t.me/c/1480232458/6825
        os.mkfifo(f'radio-{CHAT_ID}.raw')
        group_call.input_filename = f'radio-{CHAT_ID}.raw'
        if not group_call.is_connected:
            await self.start_call()
        ffmpeg_log = open("ffmpeg.log", "w+")
        command=["ffmpeg", "-y", "-i", station_stream_url, "-f", "s16le", "-ac", "2",
        "-ar", "48000", "-acodec", "pcm_s16le", group_call.input_filename]

        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=ffmpeg_log,
            stderr=asyncio.subprocess.STDOUT,
            )

        FFMPEG_PROCESSES[CHAT_ID] = process
        await self.edit_title(station_stream_url)
        await sleep(2)
        while True:
            if group_call.is_connected:
                print("Succesfully Joined VC !")
                break
            else:
                print("Connecting, Please Wait ...")
                await self.start_call()
                await sleep(10)
                continue


    async def stop_radio(self):
        group_call = self.group_call
        if group_call:
            playlist.clear()   
            group_call.input_filename = ''
            try:
                RADIO.remove(1)
            except:
                pass
            try:
                RADIO.add(0)
            except:
                pass
        process = FFMPEG_PROCESSES.get(CHAT_ID)
        if process:
            try:
                process.send_signal(SIGINT)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                print(e)
                pass
            FFMPEG_PROCESSES[CHAT_ID] = ""


    async def start_call(self):
        group_call = self.group_call
        try:
            await group_call.start(CHAT_NAME)
        except FloodWait as e:
            await sleep(e.x)
            if not group_call.is_connected:
                await group_call.start(CHAT_NAME)
        except GroupCallNotFoundError:
            try:
                await USER.send(CreateGroupCall(
                    peer=(await USER.resolve_peer(CHAT_NAME)),
                    random_id=randint(10000, 999999999)
                ))
                await group_call.start(CHAT_NAME)
            except Exception as e:
                print(e)
                pass
        except Exception as e:
            print(e)
            pass


    async def edit_title(self, station_stream_url):
        title = f'{RADIO_TITLE} [{station_stream_url}]'
        call = InputGroupCall(id=self.group_call.group_call.id, access_hash=self.group_call.group_call.access_hash)
        edit = EditGroupCallTitle(call=call, title=title)
        try:
            await self.group_call.client.send(edit)
        except Exception as e:
            print("Error Occured On Changing VC Title:", e)
            pass


    async def delete(self, message):
        if message.chat.type == "supergroup":
            await sleep(DELAY)
            try:
                await message.delete()
            except:
                pass


    async def get_admins(self, chat):
        admins = ADMIN_LIST.get(chat)
        if not admins:
            admins = Config.ADMINS
            try:
                grpadmins=await bot.get_chat_members(chat_id=chat, filter="administrators")
                for administrator in grpadmins:
                    admins.append(administrator.user.id)
            except Exception as e:
                print(e)
                pass
            ADMIN_LIST[chat]=admins
        return admins



mp = MusicPlayer()

# pytgcalls handlers

@mp.group_call.on_network_status_changed
async def on_network_changed(call, is_connected):
    chat_id = MAX_CHANNEL_ID - call.full_chat.id
    if is_connected:
        CALL_STATUS[chat_id] = True
    else:
        CALL_STATUS[chat_id] = False

@mp.group_call.on_playout_ended
async def playout_ended_handler(_, __):
    await mp.start_radio()
