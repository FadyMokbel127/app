from telethon.sync import TelegramClient
from telethon import events
from datetime import datetime
from telethon.tl.types import UserStatusOnline
from telethon.tl.types import UserStatusOffline
import asyncio

# Your Telegram API credentials
api_id = '29979621'
api_hash = '9085aa408086250f80be0b50f1fc57fd'

# Your phone number (with the country code, e.g., +1 for the US)
phone_number = '+201211255244'

# Target user's username or phone number
target_username = '+201225365145'

async def main():
    async with TelegramClient('session_name', api_id, api_hash) as client:
        # Connect to Telegram
        print("Connecting to Telegram...")
        await client.start(phone_number)

        # Get information about the target user
        try:
            target_user = await client.get_entity(target_username)
            username = target_user.username
            print(f"User '{username}' found.")
        except Exception as e:
            print(f"Error: {e}")
            return

        # Open the log file in append mode
        with open("D:\Python\TeleLog\Log.txt", "a") as file:
            @client.on(events.UserUpdate)
            async def handler(event):
                # Check if the event is related to the target user being online
                if event.user_id == target_user.id:
                    if isinstance(event.status, UserStatusOnline):
                        do = datetime.now()
                        onl = f'{username} Online {do}'
                        print(onl)
                        file.write(f'{onl}\n')
                        file.flush()
                    elif event.typing or event.recording or event.uploading:
                        return
                    elif isinstance(event.status, UserStatusOffline):
                        dof = datetime.now()
                        offl = f'{username} Offline {dof}' 
                        print(offl)
                        file.write(f'{offl}\n')
                        file.flush()

            # Run the event handler
            await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
