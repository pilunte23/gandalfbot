#file  -- function.py --
import discord
import json
def emoji(bot,emoji_name):
    emoji = discord.utils.get(bot.emojis, name=emoji_name)
    return str(emoji)





