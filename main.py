import time

import discord
from discord import Message

from bot import commands, conf


BOT_TOKEN = conf.BOT_TOKEN
PREFIX = conf.BOT_PREFIX


class MyClient(discord.Client):
    async def on_ready(self):
        print('------')
        print('Logged on as {0}!'.format(self.user))
        print('------\nServers:')
        for guild in self.guilds:
            print(guild)
        print('------')

    async def on_message(self, message: Message):
        if message.author.bot:
            if message.author == self.user:
                time.sleep(5)
                await message.delete()

            return

        print('Message:', f'Text: {message.content}', f'Server: {message.guild}')

        if message.content.startswith(f'{PREFIX}hello'):
            await commands.hello_world(message)

        if message.content.startswith(f'{PREFIX}clear'):
            await commands.clear(message)


client = MyClient()
client.run(BOT_TOKEN)
