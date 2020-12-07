import discord
import os
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Создание глобальных переменных
client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    msg = message.content.split()

    if message.author == client.user:
        return

    if message.content.startswith('!clear'):

        if message.author.guild_permissions.manage_messages:

            await message.channel.purge(limit=1)

            try:
                amount = int(msg[1])
                await message.channel.purge(limit=amount)
                await message.channel.send(f"Я удалил {amount} сообщений, Sir!")

            except:
                amount = 1
                await message.channel.purge(limit=amount)
                await message.channel.send(f"Я удалил {amount} сообщений, Sir!")

            time.sleep(1.25)
            await message.channel.purge(limit=1)

        else:

            await message.channel.send('У вас нет прав!')
            time.sleep(1.25)
            await message.channel.purge(limit=1)


client.run(BOT_TOKEN)
