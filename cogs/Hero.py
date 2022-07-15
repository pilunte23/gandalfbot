import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import *
from unidecode import unidecode
from PIL import Image
import json
import re
import asyncio
import os
import random

class Hero(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="h",
        description="Tirage des Héros aléatoires",
        guild_ids=list(map(int,str(os.getenv("GUILDID")).split(" "))),
        options=[  
            create_option(
                name="hero_1",
                description="Sphère du premier héro (Commandement,Connaissance,Energie,Tactique,Neutre...)",
                required=False,
                option_type=3,
                choices=[
                    create_choice(
                        name="Aléatoire (par défaut)",
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
                name="hero_2",
                description="Sphère du second héro (Commandement,Connaissance,Energie,Tactique,Neutre...)",
                required=False,
                option_type=3,
                choices=[
                    create_choice(
                        name="Aléatoire (par défaut)",
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
                    ),
                    create_choice(
                        name="Pas de second héro",
                        value="no"
                    )
                ]
            ),
             create_option(
                name="hero_3",
                description="Sphère du troisième héro (Commandement,Connaissance,Energie,Tactique,Neutre...)",
                required=False,
                option_type=3,
                choices=[
                    create_choice(
                        name="Aléatoire (par défaut)",
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
                    ),
                    create_choice(
                        name="Pas de troisième héro",
                        value="no"
                    )
                ]
            )
        ]     
    )

    async def _carte(self,ctx,hero_1="all",hero_2= "all",hero_3="all"):
        "pas de multilingue pour l'instant"
        langue="fr"
        resultat_carte = []
        list_hero1 = []
        list_hero2 = []
        list_hero3 = []
        img = []
        place = 0
        img_weight = 0
        url_file =  "./data/sda_"+langue+".json"
        f = open(url_file)
        dataCard = json.load(f)       
        for i in dataCard:
            if i["type_code"] == "hero": 
                if i["pack_code"] not in ["EoL", "DoG", "RoR", "DoD"]:
                    if "ALeP" not in i["pack_name"]:
                        if "(MotK)" not in i["name"]:
                            if (i["sphere_code"] == hero_1 or hero_1 =="all" ):
                                list_hero1.append(i)
                            if (i["sphere_code"] == hero_2 or hero_2 =="all" ) and hero_2 !="no": 
                                list_hero2.append(i)
                            if (i["sphere_code"] == hero_3 or hero_3 =="all" ) and hero_3 !="no":
                                list_hero3.append(i)
        randomHero1 = random.randint(0, len(list_hero1)-1)
        resultat_carte.append(list_hero1[randomHero1])  
        
        if hero_2 !="no":
            randomHero2 = random.randint(0, len(list_hero2)-1) 
            while list_hero1[randomHero1]["name"] == list_hero2[randomHero2]["name"]:
                randomHero2 = random.randint(0, len(list_hero2)-1)
            resultat_carte.append(list_hero2[randomHero2])

        if hero_3 !="no":
            randomHero3 = random.randint(0, len(list_hero3)-1)
            if hero_2 =="no":  
                while list_hero1[randomHero1]["name"] == list_hero3[randomHero3]["name"]:
                    randomHero3 = random.randint(0, len(list_hero3)-1)
            else:
                while list_hero1[randomHero1]["name"] == list_hero3[randomHero3]["name"] or list_hero2[randomHero2]["name"] == list_hero3[randomHero3]["name"]:
                    randomHero3 = random.randint(0, len(list_hero3)-1) 
            resultat_carte.append(list_hero3[randomHero3]) 

        """ define the size of the result with the number of card found """
        img_weight = (img_weight + len(resultat_carte)) * 493
        img_height = 700
        """ add every patch in the list img """
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
                  
def setup(bot):
    bot.add_cog(Hero(bot))