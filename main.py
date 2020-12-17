import time                                                 # Импорт библиотек
import datetime
import discord
from discord.ext import commands
from discord.utils import get
import os


BOT_TOKEN = os.getenv("BOT_TOKEN")                          # Создание глобальных переменных
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX")
client = commands.Bot(command_prefix=COMMAND_PREFIX, help_command=None)


@client.event                                               # Включение бота
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.command()                                           # Команда "help"
async def help(ctx):
    await ctx.channel.purge(limit=1)
    if ctx.message.author.guild_permissions.administrator:
        embed = discord.Embed(title="help", description=" ", color=discord.Colour.blue())
        embed.add_field(name="Модерация сервера", value="Модерационные команды:", inline=False)
        embed.add_field(name="clear (число)", value="Удаляет заданное число сообщений", inline=False)
        embed.add_field(name="kick [пользователь] (причина)", value="Удаляет пользователя с сервера", inline=False)
        embed.add_field(name="ban [пользователь] (причина)", value="Блокирует пользователю доступ к серверу", inline=False)
        embed.add_field(name="unban [пользователь]", value="Разблокирует пользователю доступ к серверу", inline=False)
        embed.add_field(name="Управление музыкой", value="Музыкальные команды:", inline=False)
        embed.add_field(name="join", value="Подключает бота к голосовому каналу", inline=True)
        embed.add_field(name="leave", value="Отключает бота от голосового канала", inline=True)
        embed.set_footer(text="[] - обязательный аргумент, () - необязательный аргумент")
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="help", description=" ", color=discord.Colour.blue())
        embed.set_footer(text="[] - обязательный аргумент, () - необязательный аргумент")
        await ctx.send(embed=embed)


# Модерационные комманды
@client.command()                                           # Команда "clear"
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=None):
    if amount:
        amount = int(amount)+1
        await ctx.channel.purge(limit=amount)
    else:
        amount = 2
        await ctx.channel.purge(limit=amount)
    embed = discord.Embed(title=f"{COMMAND_PREFIX}clear", description=f"Удалено {amount-1} сообщений, Sir!", color=discord.Colour.green())
    await ctx.send(embed=embed)
    time.sleep(1.5)
    await ctx.channel.purge(limit=1)


@clear.error
async def clear_error(ctx, error):
    await ctx.channel.purge(limit=1)
    author = ctx.message.author
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{author.mention}, у Вас недостаточно прав для использования этой команды!\nНедостающее право: Управлять сообщениями")
        time.sleep(1)
        await ctx.channel.purge(limit=1)


@client.command()                                           # Команда "kick"
@commands.has_permissions(administrator=True)
async def kick(ctx, username: discord.Member, *, reason=None):
    if reason is None:
        reason = "No reason provided"
    await username.kick(reason=reason)
    await ctx.channel.purge(limit=1)
    await ctx.send(f"Я удалил пользователя {username.mention}, Sir!")
    time.sleep(1)
    await ctx.channel.purge(limit=1)


@kick.error
async def kick_error(ctx, error):
    await ctx.channel.purge(limit=1)
    author = ctx.message.author
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{author.mention}, у Вас недостаточно прав для использования этой команды!\nНедостающее право: Выгонять пользователей")
        time.sleep(1)
        await ctx.channel.purge(limit=1)
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"{author.mention}, вы неверно ввели аргументы комманды!")
        time.sleep(1)
        await ctx.channel.purge(limit=1)
        return
    else:
        await ctx.send(f"{author.mention}, вы ввели комманду неверно!\nВоспользуйтесь {COMMAND_PREFIX}helpme")
        time.sleep(1.25)
        await ctx.channel.purge(limit=1)
        return


@client.command()                                           # Команда "ban"
@commands.has_permissions(administrator=True)
async def ban(ctx, username: discord.Member, *, reason=None):
    if reason is None:
        reason = "No reason provided"
    await ctx.guild.ban(username, reason=reason)
    await ctx.channel.purge(limit=1)
    await ctx.send(f"Я ЗАБАНИЛ пользователя {username.mention}, Sir!")
    time.sleep(1.25)
    await ctx.channel.purge(limit=1)


@ban.error
async def ban_error(ctx, error):
    await ctx.channel.purge(limit=1)
    author = ctx.message.author
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{author.mention}, у Вас недостаточно прав для использования этой команды!\nНедостающее право: Банить пользователей")
        time.sleep(1)
        await ctx.channel.purge(limit=1)
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"{author.mention}, вы неверно ввели аргументы комманды!")
        time.sleep(1)
        await ctx.channel.purge(limit=1)
        return
    else:
        await ctx.send(f"{author.mention}, вы ввели комманду неверно!\nВоспользуйтесь {COMMAND_PREFIX}helpme")
        time.sleep(1.25)
        await ctx.channel.purge(limit=1)
        return


@client.command()                                           # Комманда "unban"
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


@unban.error
async def unban_error(ctx, error):
    await ctx.channel.purge(limit=1)
    author = ctx.message.author
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{author.mention}, у Вас недостаточно прав для использования этой команды!\nНедостающее право: Разбанивать пользователей")
        time.sleep(5)
        await ctx.channel.purge(limit=1)
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"{author.mention}, вы неверно ввели аргументы команды!")
        time.sleep(5)
        await ctx.channel.purge(limit=1)
        return
    else:
        await ctx.send(f"{author.mention}, вы ввели команду неверно!\nВоспользуйтесь {COMMAND_PREFIX}helpme")
        time.sleep(5)
        await ctx.channel.purge(limit=1)
        return


@client.command()                                           # Комманда "mute" [НЕ РАБОТАЕТ]
@commands.has_permissions(administrator=True)
async def mute(ctx, username: discord.Member):
    author = ctx.message.author
    await ctx.channel.purge(limit=1)
    if username.guild_permissions.administrator:
        await ctx.send(f"{author.mention}, вы не можете замутить BOSS OF THIS GYM!")
        time.sleep(1.25)
        await ctx.channel.purge(limit=1)
        return
    else:
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await username.add_roles(role)
        await ctx.send(f"{author.mention}, пользователь {username.mention} замучен!")


# Музыкальные комманды
@client.command()                                           # Комманда "join"
@commands.has_permissions(administrator=True)
async def join(ctx):
    await ctx.channel.purge(limit=1)
    channel = ctx.message.author.voice.channel
    if not channel:
        await ctx.send("Вы не в голосовом канале!")
        return
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await voice.disconnect()
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await ctx.send(f"Я присоединился к {channel}, Sir!")


@join.error
async def join_error(ctx, error):
    await ctx.channel.purge(limit=1)
    author = ctx.message.author
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{author.mention}, у Вас недостаточно прав для использования этой команды!\nНедостающее право: Доступ к управлению музыкой!")
        time.sleep(1)
        await ctx.channel.purge(limit=1)


@client.command()                                           # Комманда "leave"
@commands.has_permissions(administrator=True)
async def leave(ctx):
    await ctx.channel.purge(limit=1)
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send(f"Я покинул {channel}")
    else:
        await ctx.send("Я не думаю, что я в голосовом канале!")


@leave.error
async def join_error(ctx, error):
    await ctx.channel.purge(limit=1)
    author = ctx.message.author
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"{author.mention}, у Вас недостаточно прав для использования этой команды!\nНедостающее право: Доступ к управлению музыкой!")
        time.sleep(1)
        await ctx.channel.purge(limit=1)


@client.event                                               # Исключатель ошибки "Неизвестная команда" + логи в консоль
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    else:
        print(datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=3))), ':', ctx.message.author, ':', error)


client.run(BOT_TOKEN)
