#file  -- function.py --
import discord

def emoji(bot,emoji_name):
    emoji = discord.utils.get(bot.emojis, name=emoji_name)
    return str(emoji)

