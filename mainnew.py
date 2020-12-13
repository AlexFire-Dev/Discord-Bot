import discord                                                              # Импорт библиотек
from discord import Member
import os
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")                                          # Создание глобальных переменных
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX")
client = discord.Client()


@client.event                                                               # Включение бота
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event                                                               # Реакция на сообщение пользобителя
async def on_message(message):
    msg = message.content.split()

    if message.author == client.user:                                       # Реакция на сообщение бота
        return

    if message.content.startswith(f"{COMMAND_PREFIX}clear"):                # Комманда "clear"

        await message.channel.purge(limit=1)

        if message.author.guild_permissions.manage_messages:

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

    if message.content.startswith(f"{COMMAND_PREFIX}help"):                 # Комманда "help"

        await message.channel.purge(limit=1)
        await message.channel.send(f'{message.author.mention}'
                                   f'\n1. clear(число) - удаляет заданное число сообщений'
                                   f'\n2. kick [пользователь] (причина)  - удаляет пользователя с сервера'
                                   f'\n3. ban [пользователь] (причина)   - блокирует пользователю доступ к серверу'
                                   f'\n\n* [] - обязательный аргумент'
                                   f'\n* () - необязательный аргумент')

    if message.content.startswith(f"{COMMAND_PREFIX}kick"):                 # Комманда "kick"
        await message.channel.purge(limit=1)

        if message.author.guild_permissions.administrator:
            try:
                member: Member = discord.utils.find(lambda m: msg[1] in m.name, message.guild.members)
                print(member)

                try:
                    reason = msg[2]

                except:
                    reason = "Причина не указана"

                await member.kick(reason=reason)

            except:
                await message.channel.send(f"{message.author.mention}, вы ввели команду неверно, воспользуйтесь {COMMAND_PREFIX}help")

        else:
            await message.channel.send('У вас нет прав!')
            time.sleep(1.25)
            await message.channel.purge(limit=1)


client.run(BOT_TOKEN)
