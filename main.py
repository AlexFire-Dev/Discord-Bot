import discord
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content.lower().split()
    print(msg)

    if msg[0] == "!hello":
        await message.channel.send('Hello!')

client.run(BOT_TOKEN)
