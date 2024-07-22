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
import re
import sys
import subprocess
from dotenv import load_dotenv
try:
    from yt_dlp import YoutubeDL
except ModuleNotFoundError:
    file=os.path.abspath("requirements.txt")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', file, '--upgrade'])
    os.execl(sys.executable, sys.executable, *sys.argv)

load_dotenv()

ydl_opts = {
    "geo-bypass": True,
    "nocheckcertificate": True
    }
ydl = YoutubeDL(ydl_opts)

def prepareStreamUrl(streamUrl):
    match = re.match(r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+", streamUrl)
    if match:
        meta = ydl.extract_info(streamUrl, download=False)
        formats = meta.get('formats', [meta])
        links=[]
        for f in formats:
            links.append(f['url'])
        return links[0]
    else:
        return streamUrl


class Config:
    # Mendatory Variables
    ADMIN = os.environ.get("AUTH_USERS", "")
    ADMINS = [int(admin) if re.search('^\d+$', admin) else admin for admin in (ADMIN).split()]
    API_ID = int(os.environ.get("API_ID", ""))
    API_HASH = os.environ.get("API_HASH", "")
    CHAT_ID = int(os.environ.get("CHAT_ID", ""))
    CHAT_NAME = os.environ.get("CHAT_NAME", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    SESSION_NAME = os.environ.get("SESSION_NAME", "")

    # Optional Variables
    DEFAULT_STREAM_URL = prepareStreamUrl(os.environ.get("STREAM_URL", "https://stream-relay-geo.ntslive.net/stream"))
    DELAY = int(os.environ.get("DELAY", 10))
    RADIO_TITLE = os.environ.get("RADIO_TITLE", "TelegaRadio")

    # Temp DB Variables ( Don't Touch )
    msg = {}
    playlist=[]

