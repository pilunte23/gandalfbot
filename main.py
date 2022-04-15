
import os
import discord
import json
import re
import unidecode
import asyncio
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import *
from dotenv import load_dotenv
from PIL import Image


load_dotenv(dotenv_path="config")

bot = commands.Bot(command_prefix='!', case_insensitive=True)
slash = SlashCommand(bot , sync_commands=True)

def emoji(emoji_name):
    emoji = discord.utils.get(bot.emojis, name=emoji_name)
    str = emoji_name + f" {emoji}"
    return str

@bot.event
async def on_ready():
	""" check if bot is connected """
	print("Le robot est connecté comme {0.user}".format(bot))
    

@slash.slash(
    
    name="c",
    description="Pour l'affichage de carte(s)",
    guild_ids=list(map(int,str(os.getenv("GUILID")).split(" "))),
    options=[
        create_option(
            name="recherche",
            description="Nom de la carte recherchée",
            required=True,
            option_type=3
        ),
        create_option(
            name="sphere",
            description="Choix de la sphère",
            required=False,
            option_type=3,
            choices=[
                create_choice(
                    name="Pas de filtre",
                    value="all",        
                ),
                create_choice(    
                    name= "Commandement",
                    value="leadership"
                ),
                create_choice(
                    name="Connaissance",
                    value="lore"
                ),
                create_choice(
                    name="Energie",
                    value="spirit"
                ),
                create_choice(
                    name="Tactique",
                    value="tactics"
                ),
                create_choice(
                    name="Neutre",
                    value="neutral"
                ),
                create_choice(
                    name="Sacquet",
                    value="baggins"
                ),
                create_choice(
                    name="Communauté",
                    value="fellowship"
                )
            ]
        ),
        create_option(
            name="type",
            description="Type de carte",
            required=False,
            option_type=3,
            choices=[
                create_choice(
                    name="Pas de filtre",
                    value="all"
                ),
                create_choice(
                    name="Héro",
                    value="Hero"
                ),
                create_choice(
                    name="Allié",
                    value="Ally"
                ),
                create_choice(
                    name="Attachement",
                    value="Attachement"
                ),
                create_choice(
                    name="Evènement",
                    value="Event"
                ),
                create_choice(
                    name="Contrat",
                    value="Contract"
                ),
                create_choice(
                    name="Quête annexe",
                    value="Player Side Quest"
                ),
                create_choice(
                    name="Campagne",
                    value="Campaign"
                )
            ]
        ),
        create_option(
            name="multicard",
            description="Affichage multicarte",
            required=False,
            option_type=3,
            choices=[
                create_choice(
                    name="Oui",
                    value="yes"
                ),
                create_choice(
                    name="Non",
                    value="no"
                )
            ]
        )
    ]       
)

async def _carte(ctx:SlashContext, recherche:str,sphere="all",type= "all",multicard="no",search_type="name"):
    "pas de multilingue pour l'instant"
    langue="fr"
    """lower and remove accents"""
    recherche = ".*"+unidecode.unidecode(str(recherche.lower()))+".*"
    resultat_carte = []
    img = []
    place = 0
    img_weight = 0
    url_file =  "./data/sda_"+langue+".json"
    f = open(url_file)
    data = json.load(f)

    for i in data:
        """ search in name or traits"""
        if re.search(recherche,unidecode.unidecode(str(i["name"].lower()))): 
            if ( sphere == i['sphere_code'] or sphere == "all" ) and ( type == i['type_name'] or type == "all" ):
                """check exist octgn file"""
                if "octgnid" in i:
                    """ remove (MotK) card and starter deck (no octgn file) and """
                    if not (re.search("(MotK)",i['name'])) and i['pack_code'] not in ["EoL", "DoG", "RoR", "DoD"] and not (re.search("ALeP",i['pack_name'])):
                        """ check if the id is already on the list """
                        already_find = False  
                        for j in resultat_carte:
                            if i['name'] == j['name'] and i['sphere_code'] == j['sphere_code'] \
                            and i['text'] == j['text']:
                                already_find = True
                        if already_find == False:      
                            resultat_carte.append(i)                
    if len(resultat_carte) > 0:
        if len(resultat_carte) == 1:
            if langue == "fr": 
                await sendcard(ctx,resultat_carte[0])
        else:
            if multicard == "yes":
                if len(resultat_carte) > 10:
                    await _toomuchcard(ctx)
                else:
                    """ define the size of the result with the number of card found """
                    img_weight = (img_weight + len(resultat_carte)) * 493
                    img_height = 700
                    """ add every patch in the list img """
                    number_image = 1
                    for i in resultat_carte:
                        img.append(i['octgnid']+".jpg")
                    """ creating the new img who will be send """
                    new_img = Image.new('RGB', (img_weight, img_height), (250,250,250))
                    """ we paste every image in the new_img """
                    for i in img:
                        image = Image.open("./images/"+i)
                        largeur = 0+(place*493)
                        new_img.paste(image, (largeur, 0))
                        place += 1
                    """ saving the result in a png """
                    new_img.save("requête.png", "PNG")
                    """ beautiful embed """
                    embed_carte = discord.Embed(name = "Test", color = discord.Color.blue())
                    file = discord.File("requête.png", filename = "image.png")
                    embed_carte.set_image(url ="attachment://image.png")
                    await ctx.send(file=file,embed = embed_carte)
            else:
                if len(resultat_carte) > 24:
                    await _toomuchcard(ctx)
                else:
                    """menu for single card search"""
                    await _selectingbox(ctx,resultat_carte)               
    else:
        file_url = "./assets/picture/no_card.png"
        file = discord.File(file_url, filename="image.png")
        embed_no_carte = discord.Embed(name = "no result", color = discord.Color.red())
        embed_no_carte.set_image(url="attachment://image.png")
        embed_no_carte.add_field(name = "Aucune carte n'a été trouvée", value = "Vous ne passerez pas !!!")   
        no_card_msg = await ctx.send(file=file,embed = embed_no_carte)
        await asyncio.sleep(5)
        await no_card_msg.delete()

async def _toomuchcard(ctx):
    embed_too_carte = discord.Embed(name = "too much result", color = discord.Color.red())
    embed_too_carte.add_field(name = "Trop de résultat", value = "Trop de cartes trouvées, veuillez affiner votre recherche")   
    too_card_msg = await ctx.send(embed = embed_too_carte)
    await asyncio.sleep(5)
    await too_card_msg.delete()

async def _selectingbox(ctx,resultat_carte):
    list_card = []
    count = 0
    for i in resultat_carte:
        if i['sphere_code'] == "spirit":
            altsphere_emoji = "🟦"
        if i['sphere_code'] == "lore":
            altsphere_emoji = "🟩"
        if i['sphere_code'] == "leadership":
            altsphere_emoji = "🟪"
        if i['sphere_code'] == "tactics":
            altsphere_emoji = "🟥"
        if i['sphere_code'] == "neutral":
            altsphere_emoji = "⬜"
        if i['sphere_code'] == "baggins":
            altsphere_emoji = "🟨"
        if i['sphere_code'] == "fellowship":
            altsphere_emoji = "🟧" 
        list_card.append(create_select_option(i['name']+" "+ i['type_name']+" "+ i['sphere_name'], value=str(count),emoji=altsphere_emoji))
        count += 1
        select = create_select(
        options=list_card,
        placeholder="choix de la carte",
        min_values=1,
        max_values=1
    )   

    fait_ctx = await ctx.send("Choisissez votre carte", components=[create_actionrow(select)])

    def check(m):
        return m.author_id == ctx.author.id and m.origin_message.id == fait_ctx.id

    choice_ctx = await wait_for_component(bot,components=select, check=check)

    datacard = resultat_carte[int(choice_ctx.values[0])]
    await sendcard(ctx,datacard)
    await fait_ctx.delete()

async def sendcard(ctx,datacard):
    """ beautiful embed """
    if datacard['sphere_code'] == "spirit":
        sphere_color = 0x33DDFF
    if datacard['sphere_code'] == "lore":
        sphere_color = 0x0E7A12
    if datacard['sphere_code'] == "leadership":
        sphere_color = 0x8B23F9
    if datacard['sphere_code'] == "tactics":
        sphere_color = 0xDB140B
    if datacard['sphere_code'] == "neutral":
        sphere_color = 0x797B7A
    if datacard['sphere_code'] == "baggins":
        sphere_color = 0xD3D911
    if datacard['sphere_code'] == "fellowship":
        sphere_color = 0xD99611
    file_url = "./images/"+datacard['octgnid']+".jpg"
    emoji = discord.utils.get(bot.emojis, name=datacard['sphere_code'])
    if datacard['sphere_code'] == "neutral":
        embed = discord.Embed(title=datacard['name']) #creates embed
    else:
        embed = discord.Embed(title=f"{emoji} "+datacard['name'],color=sphere_color) #creates embed
    file = discord.File(file_url, filename="image.jpg")
    pack_file = discord.File(f"./assets/pack/{datacard['pack_code']}.png", filename="pack.png")
    embed.set_author(name=f"{datacard['pack_name']}", url= f"https://ringsdb.com/set/{datacard['pack_code']}")
    if datacard['has_errata']:
        errata=f"Cette carte possède une [FAQ](http://lotr-lcg-quest-companion.gamersdungeon.net/#Card{datacard['position']})"
        embed.add_field(name="\u200b",value=errata) #creates embed
    embed.set_thumbnail(url=f"attachment://pack.png")
    embed.set_image(url="attachment://image.jpg")
    await ctx.send(files=[file,pack_file], embed=embed)


bot.run(os.getenv("TOKEN"))