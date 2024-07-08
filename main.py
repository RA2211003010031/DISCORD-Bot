import os
import discord
from discord.ext import commands
import requests
from io import BytesIO
from dotenv import load_dotenv
from telegram import Bot

# Load environment variables from .env file
load_dotenv()

# Discord bot token
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Telegram bot token
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# Telegram chat ID of the group where you want to send images
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Check if environment variables are set
if not DISCORD_TOKEN:
    print("Error: Discord token not found in environment variables.")
    exit()

if not TELEGRAM_TOKEN:
    print("Error: Telegram token not found in environment variables.")
    exit()

if not TELEGRAM_CHAT_ID:
    print("Error: Telegram chat ID not found in environment variables.")
    exit()

# Initialize Discord client and bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Initialize Telegram bot
telegram_bot = Bot(token=TELEGRAM_TOKEN)

# Function to send image to Telegram
async def send_image_to_telegram(image_url):
    print("Sending image to Telegram using bot:", telegram_bot.username)
    response = requests.get(image_url)
    if response.status_code == 200:
        photo = BytesIO(response.content)
        try:
            await telegram_bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo)
            print("Image sent to Telegram successfully.")
        except Exception as e:
            print("Error sending image to Telegram:", e)

# Event listener for new messages in Discord
@bot.event
@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.TextChannel):  # Check if it's a server channel
        print("Message received in channel:", message.channel.name)
    else:
        print("Message received in DM channel")

    print("Message content:", message.content)
    
    # Check if the message contains an attachment (image)
    if message.attachments:
        print("Attachments detected:", len(message.attachments))
        for attachment in message.attachments:
            print("Attachment URL:", attachment.url)
            # if attachment.url.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                # Send the image to Telegram
            await send_image_to_telegram(attachment.url)
            print("Print in telegram function called!")
            print("Processing image:", attachment.url)
    
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    # Initialize the Telegram bot
    await telegram_bot.initialize()

# Start the Discord bot
bot.run(DISCORD_TOKEN)