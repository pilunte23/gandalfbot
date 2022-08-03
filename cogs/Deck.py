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
        #guild_ids=list(map(int,"962626468591058974")),
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
            ),
            create_option(
                name="sideboard",
                description="Afficher les cartes mise de coté ?",
                option_type=3,
                required=False,
                choices=[   create_choice(
                                name="Oui ",
                                value="yes"
                            ),
                            create_choice(
                                name="Non",
                                value="no"
                            )
                        ]
            ),
            create_option(
                name="information",
                description="Afficher des informations complémentaires ?",
                option_type=3,
                required=False,
                choices=[   create_choice(
                                name="Non",
                                value="no"
                            ),
                            create_choice(
                                name="Le nom du paquet",
                                value="pack"
                            ),
                            create_choice(
                                name="Le nom du Cycle (valeur par défaut)",
                                value="cycleshort"
                            ),
                            create_choice(
                                name="Le nom du Cycle Complet",
                                value="cycle"
                            )
                        ]
            )              
        ]
    )

    async def _deck(self,ctx,identifiant,site="cgbuilder",sideboard="no",information="cycleshort"):
        
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

        url_file =  "./data/sda_fr.json"
        f = open(url_file)
        dataCard = json.load(f)    
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
                if section_name !="Sideboard" or (section_name =="Sideboard" and sideboard=="yes"):
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
                            code=resultat_carte[0]['code']
                            if information == "no":
                                info = ""
                            if information == "pack":
                                info = resultat_carte[0]['pack_name']
                            if information == "cycle":
                                info = searchcycle(resultat_carte[0]['pack_code'],"")
                            if information == "cycleshort":
                                info = searchcycle(resultat_carte[0]['pack_code'],"short")
                            list_card = list_card + card.get("qty") + "x " + f"{emoji}[{name}](https://ringsdb.com/card/{code})"+ f" {info} \r\n,"    
                        number_card = number_card + int(card.get("qty")) 
                    if section_name !="Hero":
                        number_field = (len(list_card)//1024) + 1
                        split_list_card = list_card.split(',')
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

def chunkify(lst, n):
    return [lst[i::n] for i in range(n)]

def searchcycle(pack_code, type):   
    cycle=""
    cycleshort=""
    if pack_code in ["Starter","Core"]:
        cycle="Boite de base"
        cycleshort="Boite de base"
        "EoL", "DoG", "RoR", "DoD",
    if pack_code == "Dod":
        cycle="Starter : Les Nains de Durin"
        cycleshort="Les Nains de Durin"
    if pack_code == "EoL":
        cycle="Starter : Les Elfes de la Lorien"
        cycleshort="Les Elfes de la Lorien"
    if pack_code == "DoG":
        cycle="Starter : Les Défenseurs du Gondor"
        cycleshort="Les Défenseurs du Gondor"
    if pack_code == "RoR":
        cycle="Starter : Les Cavaliers du Rohan"
        cycleshort="Les Cavaliers du Rohan"        
    if pack_code in ["HfG","CatC","JtR","HoEM","TDM","RtM"]:
        cycle="Cycle 1 : Ombres de la Forêt Noire"
        cycleshort="Cycle 1"
    if pack_code in ["KD","TRG","RtR","WitW","TLD","FoS","SaF"]:
        cycle="Cycle 2 : Royaume de Cavenain"
        cycleshort="Cycle 2"
    if pack_code in ["HoN","AtS","TDF","EaAD","AoO","BoG","TMV"]:
        cycle="Cycle 3 : Face à l'Ombre"
        cycleshort="Cycle 3"
    if pack_code in ["VoI","TDT","TTT","TiT","NiE","CS","TAC"]:
        cycle="Cycle 4 : Le Créateur d'Anneaux"
        cycleshort="Cycle 4"
    if pack_code in ["TLR","WoE","EfMG","AtE","ToR","BoCD","TDR"]:
        cycle="Cycle 5 : Le Réveil d'Angmar"
        cycleshort="Cycle 5"
    if pack_code in ["TGH","FotS","TitD","TotD","DR","SoCH","CoC"]:
        cycle="Cycle 6 : Chasse-Rêve"
        cycleshort="Cycle 6"
    if pack_code in ["TSoH","M","RAH","BtS","TBS","DoCG","CoP"]:
        cycle="Cycle 7 : Les Haradrim"
        cycleshort="Cycle 7"
    if pack_code in ["TWoR","TWH","RAR","FitN","TGoF","MG","TFoW"]:
        cycle="Cycle 8 : Ered Mithrin"
        cycleshort="Cycle 8"
    if pack_code in ["ASitE","WaR","TCoU","CotW","UtAM","TLoS","TFoN"]:
        cycle="Cycle 9 : La Vengeance du Mordor"
        cycleshort="Cycle 9"
    if pack_code == "OHaUH":
        cycle="Extension de saga : Par Monts et par Souterrains"
        cycleshort="Par Monts et par Souterrains"
    if pack_code == "OtD":
        cycle="Extension de saga : Au Seuil de la Porte"
        cycleshort="Au Seuil de la Porte"
    if pack_code == "TBR":
        cycle="Extension de saga : Les Cavaliers Noirs"
        cycleshort="Les Cavaliers Noirs"
    if pack_code == "TRD":
        cycle="Extension de saga : La Route s'Assombrit"
        cycleshort="La Route s'Assombrit"
    if pack_code == "ToS":
        cycle="Extension de saga : La Trahison de Saroumane"
        cycleshort="La Trahison de Saroumane"
    if pack_code == "LoS":
        cycle="Extension de saga : La Terre de l'Ombre"
        cycleshort="La Terre de l'Ombre"
    if pack_code == "FotW":
        cycle="Extension de saga : La Flamme de l'Ouest"
        cycleshort="La Flamme de l'Ouest"
    if pack_code == "MoF":
        cycle="Extension de saga : La Montagne de Feu"
        cycleshort="La Montagne de Feu"
    if type=="short":
        response = cycleshort
    else:
        response = cycle
    return response

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