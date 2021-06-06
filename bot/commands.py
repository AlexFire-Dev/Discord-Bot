import discord
from discord import Message

from bot import conf


PREFIX = conf.BOT_PREFIX


async def hello_world(message: Message):
    await message.delete()
    await message.channel.send('Hello world!')


async def clear(message: Message):
    await message.delete()
    args: list = message.content.split()
    args.pop(0)
    try:
        await message.channel.purge(limit=int(args[0]))
        embed = discord.Embed(title=f'{PREFIX}clear', description=f'Удалено {int(args[0])} сообщений, Sir!', color=discord.Colour.green())
        await message.channel.send(embed=embed)
    except:
        embed = discord.Embed(title=f'{PREFIX}clear', description='Команда введена неверно!', color=discord.Colour.green())
        await message.channel.send(embed=embed)
