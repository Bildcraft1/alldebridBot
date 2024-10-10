import requests
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()
# Load the ApiKey
API_KEY = os.getenv("API_KEY")
TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ENABLED_USERS = os.getenv("ENABLED_USERS")
bot = TelegramClient('bot', TELEGRAM_API_ID, TELEGRAM_API_HASH).start(bot_token=TELEGRAM_BOT_TOKEN)


async def get_debrid_link(api_key, link):
    """Get the debrid link from AllDebrid in async way."""
    url = f"https://api.alldebrid.com/v4/link/unlock?apikey={api_key}&agent=TelegramBot&link={link}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            return data['data']['link']
        else:
            print(data)
            return False
    else:
        print(response)
        return False


@bot.on(events.NewMessage(pattern='dl *'))
async def download_link(event):
    if str(event.sender_id) in ENABLED_USERS:
        link = event.raw_text
        # if the link doesn't appear to be a link, then return
        if link.startswith("dl"):
            link = link[3:]
        if not (link.startswith("http") or link.startswith("https")):
            await event.reply("This is not a link.")
            return
        debrid_link = await get_debrid_link(API_KEY, link)
        if debrid_link:
            print("User: " + str(
                event.sender_id) + " requested link: " + link + " and got: " + debrid_link + " as a result.")
            await event.reply(f"Here is your debrid link: {debrid_link}")
        else:
            await event.reply("Something went wrong, please try again later.")
    else:
        await event.reply("You are not allowed to use this bot.")


def main():
    """Start the bot."""
    print("Starting the bot...")
    print("Loggin with id: " + str(TELEGRAM_API_ID))
    print("Enabled users: " + str(ENABLED_USERS))
    bot.run_until_disconnected()


if __name__ == '__main__':
    main()
