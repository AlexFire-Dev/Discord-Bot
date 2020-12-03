import time                                                 # Импорт библиотек
import discord
from discord.ext import commands
import os


BOT_TOKEN = os.getenv("BOT_TOKEN")                          # Создание глобальных переменных
client = commands.Bot(command_prefix='!')


@client.event                                               # Включение бота
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command()                                           # Команда "!clear"
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=None):
    if amount:
        amount = int(amount)+1
        await ctx.channel.purge(limit=amount)
    else:
        amount = 2
        await ctx.channel.purge(limit=amount)
    await ctx.send(f"Я удалил {amount-1} сообщений, Sir!")
    time.sleep(1)
    await ctx.channel.purge(limit=1)


@clear.error
async def clear_error(ctx, error):
    await ctx.channel.purge(limit=1)
    author = ctx.message.author
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{author.mention}, у Вас недостаточно прав для использования этой команды!\nНедостающее право: Управлять сообщениями")
        time.sleep(1)
        await ctx.channel.purge(limit=1)


@client.command()                                           # Команда "!kick"
@commands.has_permissions(administrator=True)
async def kick(ctx, username: discord.User):
    pass


@client.event                                               # Исключатель ошибки "Неизвестная команда"
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass


client.run(BOT_TOKEN)
