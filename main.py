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
            return

        if message.content.startswith(f'{PREFIX}clear'):
            await commands.clear(message)
            return

        if message.content.startswith(f'{PREFIX}kick'):
            await commands.kick(message)
            return

        if message.content.startswith(f'{PREFIX}unban'):
            await commands.unban(self, message)
            return

        if message.content.startswith(f'{PREFIX}ban'):
            await commands.ban(message)
            return

        if message.content.startswith(f'{PREFIX}join'):
            await commands.join(self, message)
            return

        if message.content.startswith(f'{PREFIX}leave'):
            await commands.leave(self, message)
            return


client = MyClient()
client.run(BOT_TOKEN)
