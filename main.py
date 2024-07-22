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
import asyncio
import subprocess
from time import sleep
from threading import Thread
from signal import SIGINT
from pyrogram import Client, idle
from config import Config
from utils import mp
from pyrogram.types import BotCommand, BotCommandScopeDefault


bot = Client(
    "TelegaRadioPlayer",
    Config.API_ID,
    Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="plugins.bot")
)
if not os.path.isdir("./downloads"):
    os.makedirs("./downloads")


async def main():
    async with bot:
        await mp.start_radio()

def stop_and_restart():
    bot.stop()
    sleep(10)
    os.execl(sys.executable, sys.executable, *sys.argv)


bot.run(main())
bot.start()
print("\n\nTelegaRadioPlayer Bot Started!")

bot.set_bot_commands(
    scope = BotCommandScopeDefault(),
    language_code = "en",
    commands = [
        BotCommand(
            command="start",
            description="Start The Bot"
        ),
        BotCommand(
            command="radio",
            description="Start Radio Stream by URL"
        ),
        BotCommand(
            command="stopradio",
            description="Stop Radio / Live Stream"
        ),
        BotCommand(
            command="help",
            description="Show Help Message"
        )
    ]
)


idle()
print("\n\nTelegaRadioPlayer Stopped")
bot.stop()