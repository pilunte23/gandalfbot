#file  -- function.py --
import discord

def emoji(bot,emoji_name):
    emoji = discord.utils.get(bot.emojis, name=emoji_name)
    return str(emoji)

def trad(name):
    trad=""
    if name == "Hero":
        trad = "Héro"
    if name == "Attachment":
        trad = "Attachement"
    if name == "Ally":
        trad = "Allié"
    if name == "Event":
        trad = "Evénement"
    if name == "Side Quest":
        trad = "Quête annexe joueur"
    if name == "Sideboard":
        trad = "Mise de coté"
    return trad