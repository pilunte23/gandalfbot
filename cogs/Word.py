import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import *
from unidecode import unidecode
from function import *
import json
import re
import asyncio
import os

class Word(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
    name="m",
    description="Définition de mot clé",
    guild_ids=list(map(int,str(os.getenv("GUILDID")).split(" "))),
    options=[
        create_option(
            name="motcle",
            description="mot-clé recherché",
            required=True,
            option_type=3
        )
    ]       
)

    async def _mot(self,ctx, motcle:str):
        "pas de multilingue pour l'instant"
        langue="fr"
        resultat_word = []
        url_file =  "./data/keyword_"+langue+".json"
        f = open(url_file)
        data = json.load(f)
        word_use = ".*"+ unidecode(str(motcle.lower()))+".*"
        for i in data:
            all_search = None
            all_search = re.search(word_use,unidecode(str(i["word"].lower())))
            if all_search:
                resultat_word.append(i)   
                
        if len(resultat_word) > 0:
            if len(resultat_word) == 1: 
                datacard = resultat_word[0]
                embed_word = discord.Embed(title=datacard['word'],color=discord.Color.green(),description=change(self.bot,datacard['definition']))
                await ctx.send(embed = embed_word)
            else:
                if len(resultat_word) > 24:    
                    embed_too_word = discord.Embed(name = "too much result", color = discord.Color.red())
                    embed_too_word.add_field(name = "Trop de résultat", value = "Veuillez affiner votre recherche")   
                    too_card_msg = await ctx.send(embed = embed_too_word)
                    await asyncio.sleep(5)
                    await too_card_msg.delete()
                else:
                    """menu for single word search"""
                    list_word = []
                    count = 0
                    for i in resultat_word:
                        list_word.append(create_select_option(i['word'], value=str(count)))
                        count += 1
                        select = create_select(
                        options=list_word,
                        placeholder="choix du mot-clé",
                        min_values=1,
                        max_values=1
                        )
                    fait_ctx = await ctx.send("Choisissez votre mot-clé", components=[create_actionrow(select)])
                    choice_ctx = await wait_for_component(self.bot,components=select)
                    datacard = resultat_word[int(choice_ctx.values[0])]
                    embed_word = discord.Embed(title=datacard['word'],color=discord.Color.green(),description=change(self.bot,datacard['definition']))
                    await ctx.send(embed = embed_word)
                    await fait_ctx.delete()
        else:
            file_url = "./assets/picture/no_card.png"
            file = discord.File(file_url, filename="image.png")
            embed_no_word = discord.Embed(name = "no result", color = discord.Color.red())
            embed_no_word.set_image(url="attachment://image.png")
            embed_no_word.add_field(name = "Ce mot-clé n'a été trouvé", value = "Vous ne passerez pas !!!")   
            no_card_msg = await ctx.send(file=file,embed = embed_no_word)
            await asyncio.sleep(5)
            await no_card_msg.delete()

def change(bot,str):
    str = str.replace("(defense)","("+emoji(bot,"defense") +")")
    str = str.replace("(attaque)","("+ emoji(bot,"attack") +")")
    str = str.replace("(volonte)","("+ emoji(bot,"willpower") +")")
    str = str.replace("(menace)","("+ emoji(bot,"threat") +")")
    str = str.replace("(pointdevie)","("+ emoji(bot,"hitpoints") +")")
    return str

def setup(bot):
    bot.add_cog(Word(bot))