import nextcord 
from nextcord.ext import commands
from nextcord import Interaction, SelectOption, ui, SlashOption, Embed, File
from unidecode import unidecode
from PIL import Image
import json
import re
import os
import share
import shutil
import random
import requests
import xml.etree.ElementTree as ET

class Deck(commands.Cog):

    def __init__(self, bot):
        self.bot:  commands.bot = bot

    @nextcord.slash_command(name="deck",description="Affichage d'un deck du  Seigneur des anneaux JCE",guild_ids=list(map(int,str(os.getenv("GUILDID")).split(" "))))
    async def _hero(self, interaction: Interaction, 
    identifiant: str = SlashOption(name="identifiant",description="Numéro du deck a partager", required=True),
    site: str = SlashOption(name="site",description="Sur quel site a été fait le deck ?", required=False,choices=["sda.cgbuilder.fr (par défaut)","Ringsdb.com"]),
    sideboard: str = SlashOption(name="sideboard",description="Afficher les cartes mise de coté ?", required=False,choices=["Non (par défaut)","Oui"])):
        print(f"{interaction.user} use Deck slash command" )
        if site=="Ringsdb.com":
            site="ringsdb"
        else:
            site="cgbuilder"
        if sideboard=="Non (par défaut)":
            sideboard="no"
        else:
            sideboard="yes"
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
            #filepage=requests.get(urlpage)
            #open('mypage.html','wb').write(filepage.content) 
            #url = "mypage.html"
            #page = open(url)
            #soup = BeautifulSoup(page.read(),features="html.parser")
            #mydiv=soup.find("div", {"class": "titre_partage"})
            #title=mydiv.find("h2",recursive=False).text
            #title=title.rstrip(title[-1])
            #divauthor=mydiv.find("h3",recursive=False)
            #author=divauthor.find("span",recursive=False).text
            open('mydeck.xml','wb').write(file.content)

            url_file =  "./data/SDA_carte_joueur.json"
            f =  open(url_file , encoding="utf8")
            dataCard = json.load(f) 
            embed_deck = Embed(title = title,url=urlpage)
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
                        find=False
                        resultat_carte= []               
                        for i in dataCard:
                            if 'id_octgn' in i and find == False:
                                if  card.get("id") == i['id_octgn']:
                                    resultat_carte.append(i)
                                    find=True
                                if (section_name =="Hero" or section_name =="Contract") and card.get("id") == i['id_octgn']:
                                    resultat_carte_hero.append(i)       
                        if len(resultat_carte) == 0:
                            print("non trouvé pour : "+ card.get("id"))
                            list_card = list_card + card.get("qty") + " " + card.get("id") + "\r\n"
                        else:     
                            name=resultat_carte[0]['titre']
                            id_extension=resultat_carte[0]['id_extension']
                            numero_identification=resultat_carte[0]['numero_identification']
                            cycle=share.info_cycle(resultat_carte[0],"short")
                            card_sphere, sphere_color, sphere_emoji = share.info_sphere(self,resultat_carte[0])
                            list_card = list_card + card.get("qty") + "x " + f"{sphere_emoji}[{name}](https://sda-src.cgbuilder.fr/images/carte/{id_extension}/{numero_identification}.jpg)"+ f" {cycle} \r\n;"    
                        number_card = number_card + int(card.get("qty")) 
                    number_field = (len(list_card)//1024) + 1
                    split_list_card = list_card.split(';')
                    chunks =chunkify(split_list_card, number_field)
                    i=0
                    while i < number_field:
                        list_card = ''.join(chunks[i])
                        if i == 0:
                            embed_deck.add_field(name = trad(section.get("name")) +" ("+ str(number_card)+")", value = list_card,inline=False)
                        else:
                            embed_deck.add_field(name = trad(section.get("name")) +" (Suite)", value = list_card,inline=False)
                        i = i+1

            img = []
            place = 0
            img_weight = 0
            img_weight = len(resultat_carte_hero) * 394
            img_height = 560
            """ add every patch in the list img """
            for i in resultat_carte_hero:
                print(i['titre'])
                file_url = f"./sda_cgbuilder/images/simulateur/carte/"+i['id_extension']+"/"+i['numero_identification']+".jpg"
                if os.path.isfile(file_url):
                    img.append(file_url)
                file_url = f"./sda_cgbuilder/images/simulateur/carte/"+i['id_extension']+"/"+i['numero_identification']+"A.jpg"
                if os.path.isfile(file_url):
                    img.append(file_url)
                file_url = f"./sda_cgbuilder/images/simulateur/carte/"+i['id_extension']+"/"+i['numero_identification']+"B.jpg"
                if os.path.isfile(file_url):
                    img.append(file_url)
            """ creating the new img who will be send """
            new_img = Image.new('RGB', (img_weight, img_height), (250,250,250))
            """ we paste every image in the new_img """
            for i in img:
                image = Image.open("./"+i)
                largeur = 0+(place*394)
                new_img.paste(image, (largeur, 0))
                place += 1
            """ saving the result in a png """
            new_img.save("hero.png", "PNG")
            """ beautiful embed """
            file = File("hero.png", filename = "image.png")
            embed_deck.set_image(url ="attachment://image.png")
            await interaction.send(files=[file], embed=embed_deck)

        if site=="ringsdb":
            urlo8d = 'https://ringsdb.com/decklist/export/octgn/'+ identifiant
            file=requests.get(urlo8d)
            title="Deck " +identifiant +" sur ringsdb.com"
            urlpage = "https://ringsdb.com/decklist/view/"+ identifiant
            #filepage=requests.get(urlpage)
            #open('mypage.html','wb').write(filepage.content) 
            #url = "mypage.html"
            #page = open(url)
            #soup = BeautifulSoup(page.read(),features="html.parser")
            #title=soup.find("h1", {"class": "decklist-name bg-sphere text-center"}).find(text=True, recursive=False)
            #divauthor=soup.find("h3",{"class": "username"})
            #author=divauthor.find("a").text
            #print(author)
            open('mydeck.xml','wb').write(file.content)

            url_file =  "./data/RingsDB.json"
            f =  open(url_file , encoding="utf8")
            dataCard = json.load(f) 
            embed_deck = Embed(title = title,url=urlpage)
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
                        find=False
                        resultat_carte= []               
                        for i in dataCard:
                            if 'octgnid' in i and find == False:
                                if  card.get("id") == i['octgnid']:
                                    resultat_carte.append(i)
                                    find=True
                                if (section_name =="Hero" or section_name =="Contract") and card.get("id") == i['octgnid']:
                                    resultat_carte_hero.append(i)       
                        if len(resultat_carte) == 0:
                            print("non trouvé pour : "+ card.get("id"))
                            list_card = list_card + card.get("qty") + " " + card.get("id") + "\r\n"
                        else:     
                            name=resultat_carte[0]['name']
                            code=resultat_carte[0]['code']
                            cycle=share.info_cycle_ringsdb(resultat_carte[0],"short")
                            card_sphere, sphere_color, sphere_emoji = share.info_sphere_ringsdb(self,resultat_carte[0])
                            list_card = list_card + card.get("qty") + "x " + f"{sphere_emoji}[{name}](https://ringsdb.com/card/{code})"+ f" {cycle} \r\n;"    
                        number_card = number_card + int(card.get("qty")) 
                    number_field = (len(list_card)//1024) + 1
                    split_list_card = list_card.split(';')
                    chunks =chunkify(split_list_card, number_field)
                    i=0
                    while i < number_field:
                        list_card = ''.join(chunks[i])
                        if i == 0:
                            embed_deck.add_field(name = trad(section.get("name")) +" ("+ str(number_card)+")", value = list_card,inline=False)
                        else:
                            embed_deck.add_field(name = trad(section.get("name")) +" (Suite)", value = list_card,inline=False)
                        i = i+1
            
            img = []
            place = 0
            img_weight = 0
            """ define the size of the result with the number of card found """
            img_weight = (img_weight + len(resultat_carte_hero)) * 423
            img_height = 600
            """ add every patch in the list img """
            for i in resultat_carte_hero:
                img.append(i['octgnid']+".jpg")
            """ creating the new img who will be send """
            new_img = Image.new('RGB', (img_weight, img_height), (250,250,250))
            """ we paste every image in the new_img """
            for i in img:
                if os.path.isfile("./ringsdb/"+i):
                    image = Image.open("./ringsdb/"+i)
                    largeur = 0+(place*423)
                    new_img.paste(image, (largeur, 0))
                    place += 1
            """ saving the result in a png """
            new_img.save("hero.png", "PNG")

            file = File("hero.png", filename = "image.png")
            embed_deck.set_image(url ="attachment://image.png")
            await interaction.send(files=[file], embed=embed_deck)

def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]

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
    if name == "Contract":
        trad = "Contrat"    
    return trad

def setup(bot):
    bot.add_cog(Deck(bot))