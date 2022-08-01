import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import *
import os
import requests
import xml.etree.ElementTree as ET
import json
from PIL import Image

class Deck(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="d",
        description="Partage un deck mis en ligne",
        guild_ids=list(map(int,str(os.getenv("GUILDID")).split(" "))),
        options=[
            create_option(
                name="identifiant",
                description="Numéro du deck a partager",
                required=True,
                option_type=3
            ),  
            create_option(
                name="site",
                description="Sur quel site a été fait le deck ?",
                option_type=3,
                required=False,
                choices=[   create_choice(
                                name="sda.cgbuilder.fr (par défaut)",
                                value="cgbuilder"
                            ),
                            create_choice(
                                name="Ringsdb.com",
                                value="ringsdb"
                            )
                        ]
            )             
        ]
    )

    async def _deck(self,ctx,identifiant,site="cgbuilder"):   
        if site=="cgbuilder":
            data = {
                'id_ajax': 'exporter_deck_octgn',
                'id_deck_builder': identifiant,
                'libelle': 'mydeck'
            }
            urlo8d = requests.post('https://sda.cgbuilder.fr//ajax/', data=data)
            file=requests.get(urlo8d.content)      
        if site=="ringsdb":
            urlo8d = 'https://ringsdb.com/decklist/export/octgn/'+ identifiant
            file=requests.get(urlo8d)
        open('mydeck.xml','wb').write(file.content)

        url_file =  "./data/sda_fr.json"
        f = open(url_file)
        dataCard = json.load(f)    

        embed_deck = discord.Embed(name = "", color = discord.Color.blue())
        resultat_carte_hero= []
        
        tree = ET.parse('mydeck.xml')
        root = tree.getroot()
        for section in root:
            section_name = section.get("name")
            countcard = section.findall("card")
            number_card = len(countcard)
            if number_card > 0:
                list_card = ""
                for card in section:
                    resultat_carte= []               
                    for i in dataCard:
                        if 'octgnid' in i:
                            if  card.get("id") == i['octgnid']:
                                resultat_carte.append(i)
                            if section_name =="Hero" and card.get("id") == i['octgnid']:
                                resultat_carte_hero.append(i)        
                    if len(resultat_carte) == 0:
                        print("non trouvé pour : "+ card.get("id"))
                        list_card = list_card + card.get("qty") + " " + card.get("id") + "\r\n"
                    else:     
                        emoji = discord.utils.get(self.bot.emojis, name=resultat_carte[0]['sphere_code'])
                        list_card = list_card + card.get("qty") + "x " + f"{emoji} "+resultat_carte[0]['name'] + "\r\n"
                if section_name !="Hero":
                    embed_deck.add_field(name = discord.utils.get(self.bot.trad, name=section.get("name")) +" ("+ str(number_card)+")", value = list_card)
        
        img = []
        place = 0
        img_weight = 0
        """ define the size of the result with the number of card found """
        img_weight = (img_weight + len(resultat_carte_hero)) * 493
        img_height = 700
        """ add every patch in the list img """
        for i in resultat_carte_hero:
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
        new_img.save("hero.png", "PNG")
        """ beautiful embed """
        file = discord.File("hero.png", filename = "image.png")
        embed_deck.set_image(url ="attachment://image.png")
        await ctx.send(file=file,embed = embed_deck)  

def setup(bot):
    bot.add_cog(Deck(bot))