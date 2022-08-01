from cgitb import text
from turtle import title
import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import *
from unidecode import unidecode
import os
import requests
import xml.etree.ElementTree as ET
import json
from PIL import Image
from bs4 import BeautifulSoup

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

    async def _deck(self,ctx,identifiant,site="cgbuilder",sideboard="no"):
        
        if site=="cgbuilder":
            
            data = {
                'id_ajax': 'exporter_deck_octgn',
                'id_deck_builder': identifiant,
                'libelle': 'mydeck'
            }
            urlo8d = requests.post('https://sda.cgbuilder.fr//ajax/', data=data)
            file=requests.get(urlo8d.content) 
            title="Deck " +identifiant +" sur sda.cgbuilder.fr"
            urlpage = "https://sda.cgbuilder.fr/partage_deck/"+ identifiant +"/" 
            """
            while True:
                try:
                    urlpage = "https://sda.cgbuilder.fr/partage_deck/"+ identifiant +"/"
                    filepage=requests.get(urlpage)
                    open('mypage.html','wb').write(filepage.content) 
                    url = "mypage.html"
                    page = open(url)
                    soup = BeautifulSoup(page.read(),features="html.parser")
                    mydiv=soup.find("div", {"class": "titre_partage"})
                    title=mydiv.find("h2",recursive=False).text
                    title=title.rstrip(title[-1])
                    author=mydiv.find("h3",recursive=False).text
                    urlauthor = 'https://sda.cgbuilder.fr/deck_communautaire/'+ author +'/'
                except:
                    
            """

        if site=="ringsdb":
            
            urlo8d = 'https://ringsdb.com/decklist/export/octgn/'+ identifiant
            file=requests.get(urlo8d)
            title="Deck " +identifiant +" sur ringsdb.com"
            urlpage = "https://ringsdb.com/decklist/view/"+ identifiant
            """
            while True:
                try:
                    urlpage = "https://ringsdb.com/decklist/view/"+ identifiant
                    filepage=requests.get(urlpage)
                    open('mypage.html','wb').write(filepage.content) 
                    url = "mypage.html"
                    page = open(url)
                    soup = BeautifulSoup(page.read(),features="html.parser")
                    title=soup.find("h1", {"class": "decklist-name bg-sphere text-center"}).find(text=True, recursive=False)
                    author=soup.find("a",{"class": "username"}).text
                    urlauthor = 'https://sda.cgbuilder.fr/deck_communautaire/'+ author +'/'
                except:
                    
            """

        open('mydeck.xml','wb').write(file.content)

        url_file =  "./data/sda_fr.json"
        f = open(url_file)
        dataCard = json.load(f)    
        embed_deck = discord.Embed(title = title,color = discord.Color.blue())
        embed_deck = discord.Embed(title = title,url=urlpage,color = discord.Color.blue())
        #embed_deck.set_author(name=author)
        resultat_carte_hero= []
        
        tree = ET.parse('mydeck.xml')
        root = tree.getroot()
        for section in root:
            section_name = section.get("name")
            countcard = section.findall("card")
            number_card = 0
            if len(countcard) > 0:
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
                        name=resultat_carte[0]['name']
                        list_card = list_card + card.get("qty") + "x " + f"{emoji}{name}"+ "\r\n"
                        if len(list_card) > 900:
                           embed_deck.add_field(name = trad(section.get("name")), value = list_card)
                           list_card = ""
                    number_card = number_card + int(card.get("qty")) 
                if section_name !="Hero":  
                    embed_deck.add_field(name = trad(section.get("name")) +" ("+ str(number_card)+")", value = list_card)
        
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

def setup(bot):
    bot.add_cog(Deck(bot))