import nextcord 
from nextcord.ext import commands
from nextcord import Interaction, SelectOption, ui, SlashOption, Embed, File
from unidecode import unidecode
from PIL import Image
import json
import re
import os
import share

class myselect(ui.Select):
    def __init__(self,list_card,bot):
        selectoptions = list_card
        self.bot = bot
        super().__init__(placeholder="Quelle carte voulez vous afficher? ",min_values=1,max_values=1 ,options=selectoptions)
        
    async def callback(self, interaction: Interaction):
        id= self.values[0].split("/")
        id_extension = id[0]
        numero_identification = id[1]
        url_file =  "./data/SDA_carte_joueur.json"
        f =  open(url_file , encoding="utf8")
        rawdata = json.load(f)
        data = []
        for i in rawdata:
            if i['numero_identification'] == numero_identification and i['id_extension'] == id_extension:
                data.append(i)
        return await share.sendcard(self,interaction,data[0])
      
class SelectView(ui.View):
    def __init__(self,list_card,bot):
        super().__init__()
        self.bot = bot
        self.add_item(myselect(list_card,bot))

class Player(commands.Cog):

    def __init__(self, bot):
        self.bot:  commands.bot = bot

    @nextcord.slash_command(name="c",description="Pour l'affichage de carte(s) joueur",guild_ids=list(map(int,str(os.getenv("GUILDID")).split(" "))))
    async def _timing(self, 
    interaction: Interaction, 
    recherche: str = SlashOption(name="recherche",description="Terme Recherché", required=True),
    type: str = SlashOption(name="type",description="Filtre sur le Type de Carte (Héro, Allié, Attachement, Evènement...)",required=False,choices=["Pas de filtre (par défaut)","Héro","Allié","Evènement","Attachement","Objectif Allié","Trésor","Quête Annexe Joueur","Navire Objectif","Objectif Héros","Contrat"]),
    sphere: str = SlashOption(name="sphere",description="Filtre sur la Sphère (Commandement,Connaissance,Energie,Tactique,Neutre...)",required=False,choices=["Pas de filtre (par défaut)","Commandement","Tactique","Energie","Connaissance","Neutre","Sacquet","Communauté"]),
    champs: str = SlashOption(name="champs",description="Sur Quel Champs de Rechercher le Terme saisi (Nom, Traits)",required=False, choices=["Titre (par défaut)", "Trait"]),  
    selection: str = SlashOption(name="selection",description="Type d'affichage (Liste Déroulante ou Multicarte)",required=False, choices=["Renvoie une liste de carte via Menu sélectionnable limité à 25 cartes (par défaut)", "Renvoie une image de plusieurs cartes limité à 10 cartes"]),
    terme: str = SlashOption(name="terme",description="Terme Exacte ou Partiel",required=False, choices=["Terme partiel (par défaut)", "Terme exact"])):
        #Retravaille des champs saisie par la commande
        if type == None or type =="Pas de filtre (par défaut)": 
            id_type = "all"
        else:
            id_type = share.get_id_type_carte(type)
        if sphere == None or sphere == "Pas de filtre (par défaut)":
            id_sphere = "all"
        else:
            id_sphere = share.get_id_sphere(sphere)    
        if champs == None or champs =="Titre (par défaut)":
            champs = "Titre"
        else:
            champs = "Trait"
        if terme == None or terme =="Terme partiel (par défaut)": 
            terme ="Partiel"
        else:
            terme = "Exact"
        if selection == None or selection == "Renvoie une liste de carte via Menu sélectionnable limité à 25 cartes (par défaut)" : 
            selection = "menu" 
        else: 
            selection = "multicard"
         
        #Initialisation des variables 
        resultat_carte = []
        img = []
        place = 0
        img_weight = 0
        url_file =  "./data/SDA_carte_joueur.json"
        f =  open(url_file , encoding="utf8")
        rawdata = json.load(f)
        #exclusion les Two-Player Limited Edition et les éditions révisées
        #exclusion allié-héros
        data = []
        for i in rawdata:
            if i['id_extension'] not in ['67', '87', '82', '83', '84', '88', '91', '92'] and "&bull" not in i['titre']:
                data.append(i)
        #regex differentes selon qu'on cherme un bout de mot ou le mot complet
        if terme =="Exact":
            word_use = "^"+ unidecode(str(recherche.lower()))+"$"
        else:
            #pour un Trait , la recherche sera forcement partiel parce qu'il ya toujours . à trainer et potentiellement d'autres traits
            if champs == "Trait":
                word_use = ".*\\b"+ unidecode(str(recherche.lower()))+"\\b.*"
            else:       
                word_use = ".*"+ unidecode(str(recherche.lower()))+".*"
        for i in data:
            row_search = None
            """ search in name, traits"""  
            if champs == "Titre" and "titre" in i:
                row_search = re.search(word_use,unidecode(str(i["titre"].lower()))) 
            if champs == "Trait" and "trait" in i and i["trait"] != None:
                row_search = re.search(word_use,unidecode(str(i["trait"].lower())))
            if row_search: 
                if (( id_type == i["id_type_carte"] or id_type == "all" ) and( id_sphere == i["id_sphere_influence"] or id_sphere == "all" )):   
                    resultat_carte.append(i) 
        #print("nombre de carte : " + str(len(resultat_carte)))
        if len(resultat_carte) > 0:
            if len(resultat_carte) == 1:
                await share.sendcard(self,interaction,resultat_carte[0])
            else:
                if selection == "multicard":
                    if len(resultat_carte) > 10:
                        await _toomuchcard(self,interaction)
                    else:
                        card_sphere, sphere_color, sphere_emoji = share.info_sphere(self,resultat_carte[0])
                        """ define the size of the result with the number of card found """
                        img_weight = (img_weight + len(resultat_carte)) * 394
                        img_height = 560
                        """ add every patch in the list img """
                        for i in resultat_carte:
                            src_file="sda_cgbuilder/images/simulateur/carte/"+i['id_extension']+"/"+i['numero_identification']+".jpg"
                            img.append(src_file)
                        """ creating the new img who will be send """
                        new_img = Image.new('RGB', (img_weight, img_height), (250,250,250))
                        """ we paste every image in the new_img """
                        for i in img:
                            image = Image.open("./"+i)
                            largeur = 0+(place*394)
                            new_img.paste(image, (largeur, 0))
                            place += 1
                        """ saving the result in a png """
                        new_img.save("requête.png", "PNG")
                        """ beautiful embed """
                        embed_carte = Embed(title = "Résulat pour les cartes "+(type+" " if id_type != "all" else "") + (sphere_emoji+" " if id_sphere != "all" else "") + "ayant pour"+ (" Titre " if champs == "Titre" else " Trait ") + recherche.capitalize(), color=sphere_color)
                        file = File("requête.png", filename = "image.png")
                        embed_carte.set_image(url ="attachment://image.png")
                        await interaction.send(files=[file], embed=embed_carte)
                if selection == "menu":  
                    if len(resultat_carte) > 24:
                        await _toomuchcard(self,interaction)
                    else:
                        #menu for single card search
                        await _selectingbox(self,interaction,resultat_carte)                  
        else:
            file_url = "./assets/picture/no_card.png"
            file = File(file_url, filename="image.png")
            embed_no_carte = Embed(title = "no result", color = nextcord.Color.red())
            embed_no_carte.set_image(url="attachment://image.png")
            embed_no_carte.add_field(name = "Aucune carte n'a été trouvée", value = "Vous ne passerez pas !!!")   
            await interaction.send(file=file,embed = embed_no_carte,delete_after= 5)


async def _toomuchcard(self,interaction : Interaction):
    embed_too_carte = Embed(title = "too much result", color = nextcord.Color.red())
    embed_too_carte.add_field(name = "Trop de résultat", value = "Veuillez affiner votre recherche")   
    await interaction.send(embed = embed_too_carte,delete_after= 5)


async def _selectingbox(self,interaction : Interaction,resultat_carte):
    list_card = []
    count = 0
    for i in resultat_carte:
        altsphere_emoji = "⬛"
        if i['id_sphere_influence'] == "300":
            altsphere_emoji = "🟪"
        if i['id_sphere_influence'] == "301":
            altsphere_emoji = "🟩"
        if i['id_sphere_influence'] == "302":
            altsphere_emoji = "🟦"
        if i['id_sphere_influence'] == "303":
            altsphere_emoji = "🟥"
        if i['id_sphere_influence'] == "304":
            altsphere_emoji = "⬜"
        if i['id_sphere_influence'] == "305":
            altsphere_emoji = "🟧" 
        if i['id_sphere_influence'] == "306":
            altsphere_emoji = "🟨"
        list_card.append(SelectOption(label=i['titre'],description=f"{(i['lbl type carte']).capitalize()} dans {i['lbl extension']}",value=str(f"{i['id_extension']}/{i['numero_identification']}"),emoji=altsphere_emoji))
        count += 1
    view = SelectView(list_card,self.bot)
    await interaction.response.send_message(view=view,ephemeral=True)


def setup(bot):
    bot.add_cog(Player(bot))