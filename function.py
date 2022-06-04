#file  -- function.py --
import discord

def emoji(bot,emoji_name):
    emoji = discord.utils.get(bot.emojis, name=emoji_name)
    return str(emoji)
    
def change(bot,str):
    str = str.replace("(defense)","("+emoji(bot,"defense") +")")
    str = str.replace("(attaque)","("+ emoji(bot,"attack") +")")
    str = str.replace("(volonte)","("+ emoji(bot,"willpower") +")")
    str = str.replace("(menace)","("+ emoji(bot,"threat") +")")
    str = str.replace("(pointdevie)","("+ emoji(bot,"hitpoints") +")")
    return str