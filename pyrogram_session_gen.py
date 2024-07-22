import asyncio
from pyrogram import Client

print("""
Follow The Steps Below:

1. First go to my.telegram.org
2. Login using your Telegram account
3. Then click on API Development Tools
4. Create a new application, by entering the required details
5. Check your script root directory for created radio_bot.session file 
"""
)

async def main():
    api_id = int(input("ENTER API ID: "))
    api_hash = input("ENTER API HASH: ")
    async with Client("radio_bot", api_id=api_id, api_hash=api_hash) as app:
        await app.send_message(
            "me",
            "**Pyrogram Session String**:\n\n"
            f"`{await app.export_session_string()}`\n\n"
        )
        print(
            "Done, your Pyrogram Session created!"
        )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
