import discord
from discord import Message
from discord.utils import get

from bot import conf


PREFIX = conf.BOT_PREFIX


async def hello_world(message: Message):
    await message.delete()
    await message.channel.send('Hello world!')


async def clear(message: Message):
    if not message.author.guild_permissions.manage_messages:
        return

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


async def kick(message: Message):
    if not message.author.guild_permissions.administrator:
        return

    await message.delete()
    args: list = message.content.split()
    args.pop(0)

    try:
        member: discord.Member = await message.guild.fetch_member(int(args[0][3:-1]))
        try:
            reason = args[1]
        except:
            reason = None

        if member == message.author:
            raise

        await member.kick(reason=reason)
        embed = discord.Embed(title=f'{PREFIX}kick', description=f'Пользователь {member.mention} кикнут, Sir!', color=discord.Colour.dark_orange())
        await message.channel.send(embed=embed)
    except:
        embed = discord.Embed(title=f'{PREFIX}kick', description='Команда введена неверно!', color=discord.Colour.dark_orange())
        await message.channel.send(embed=embed)


async def ban(message: Message):
    if not message.author.guild_permissions.administrator:
        return

    await message.delete()
    args: list = message.content.split()
    args.pop(0)

    try:
        member: discord.Member = await message.guild.fetch_member(int(args[0][3:-1]))
        try:
            reason = args[1]
        except:
            reason = None

        if member == message.author:
            raise

        await member.ban(delete_message_days=0, reason=reason)
        embed = discord.Embed(title=f'{PREFIX}ban', description=f'Пользователь {member.mention} забанен, Sir!', color=discord.Colour.red())
        await message.channel.send(embed=embed)
    except:
        embed = discord.Embed(title=f'{PREFIX}ban', description='Команда введена неверно!', color=discord.Colour.red())
        await message.channel.send(embed=embed)


async def unban(client: discord.Client, message: Message):
    if not message.author.guild_permissions.administrator:
        return

    await message.delete()
    args: list = message.content.split()
    args.pop(0)

    try:
        member: discord.User = await client.fetch_user(int(args[0][3:-1]))
        banned_users = await message.guild.bans()
        member_name, member_discriminator = member.name, member.discriminator

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await message.guild.unban(user)
                embed = discord.Embed(title=f'{PREFIX}unban', description=f'Пользователь {member.mention} разбанен, Sir!', color=discord.Colour.green())
                await message.channel.send(embed=embed)
                return

        embed = discord.Embed(title=f'{PREFIX}unban', description='Пользователь не забанен!', color=discord.Colour.green())
        await message.channel.send(embed=embed)
    except:
        embed = discord.Embed(title=f'{PREFIX}unban', description='Команда введена неверно!', color=discord.Colour.green())
        await message.channel.send(embed=embed)


async def join(client: discord.Client, message: Message):
    if not message.author.guild_permissions.administrator:
        return

    await message.delete()

    channel = message.author.voice.channel
    if not channel:
        await message.channel.send("Вы не в голосовом канале!")
        return
    voice = get(client.voice_clients, guild=message.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await message.channel.send(f"Я присоединился к {channel}, Sir!")


async def leave(client: discord.Client, message: Message):
    if not message.author.guild_permissions.administrator:
        return

    await message.delete()

    voice = get(client.voice_clients, guild=message.guild)
    if voice and voice.is_connected():
        await voice.disconnect()

        await message.channel.send(f"Я покинул {voice.channel}")
    else:
        await message.channel.send("Я не думаю, что я в голосовом канале!")
