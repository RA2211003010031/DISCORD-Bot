import discord
import asyncio

intents = discord.Intents.default()
intents.members = True  # Enable the members intent

client = discord.Client(intents=intents)

async def start_bot():
    try:
        await client.start('NzYxNDMwNjgwOTMyNDUwMzM2.GApo68.1Oc1dd_A6tQeBQc7MGQQ-JrLYaRbPVbzKQjCUI')
    except Exception as e:
        print(f"An error occurred while starting the bot: {e}")
        await asyncio.sleep(5)  # Wait for 5 seconds before retrying
        await start_bot()  # Retry starting the bot

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_member_join(member):
    channel = client.get_channel(939346762760613998)  # Replace YOUR_CHANNEL_ID with the ID of the channel where you want the message to be sent
    message = f"Welcome {member.mention} to the server!"  # Mention the new member in the welcome message
    sent_message = await channel.send(message)
    await sent_message.delete(delay=10)  # Delete the message after 10 seconds

async def main():
    while True:
        await start_bot()

if __name__ == "__main__":
    asyncio.run(main())
