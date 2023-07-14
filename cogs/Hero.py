import nextcord 
from nextcord.ext import commands
from nextcord import Interaction, SelectOption, ui, SlashOption, Embed, File
from unidecode import unidecode
from PIL import Image
import json
import re
import os
import share
import random

class myselect(ui.Select):
    def __init__(self,list_cycle,bot):
        self.bot = bot
        selectoptions = []
        
      
        for i in list_cycle:
            selectoptions.append(SelectOption(label=i,description="",value=i))

        super().__init__(placeholder="Quelle cycle possedez vous? ",min_values=1,max_values=len(selectoptions) ,options=selectoptions)
    
    async def callback(self,interaction: Interaction):
        resultat_carte=[]
        selected_list_id = share.id_extension_by_cycle_name(self.values)
        print(selected_list_id)
        url_file =  "./data/SDA_carte_joueur.json"
        f =  open(url_file , encoding="utf8")
        rawdata = json.load(f)
        heros1 = []
        heros2 = []
        heros3 = []
        for i in rawdata:
            if i['id_extension'] in selected_list_id and i['id_type_carte']=="400" and "&bull" not in i['titre']:
                heros1.append(i)
                heros2.append(i)
                heros3.append(i)
        if heros1 != []:       
            randomHero1 = random.randint(0, len(heros1)-1)
            resultat_carte.append(heros1[randomHero1])
        if heros2 != []:       
            randomHero2 = random.randint(0, len(heros2)-1)
            while heros2[randomHero1]["titre"] == heros2[randomHero2]["titre"]:
                randomHero2 = random.randint(0, len(heros2)-1)
            resultat_carte.append(heros2[randomHero2])
        if heros3 != []:       
            randomHero3 = random.randint(0, len(heros3)-1)
            while heros1[randomHero1]["titre"] == heros3[randomHero3]["titre"] or heros2[randomHero2]["titre"] == heros3[randomHero3]["titre"]:
                randomHero3 = random.randint(0, len(heros3)-1) 
            resultat_carte.append(heros3[randomHero3])
        
        img = []
        place = 0
        img_weight = 0
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
        embed_carte = Embed(title = "Héros aléatoires")
        file = File("requête.png", filename = "image.png")
        embed_carte.set_image(url ="attachment://image.png")
        return await interaction.send(files=[file], embed=embed_carte)
    
class SelectView(ui.View):
    def __init__(self,list_cycle,bot):
        super().__init__()
        self.bot = bot
        self.add_item(myselect(list_cycle,bot))

class Hero(commands.Cog):

    def __init__(self, bot):
        self.bot:  commands.bot = bot

    @nextcord.slash_command(name="h",description="Tirage des Héros aléatoires",guild_ids=list(map(int,str(os.getenv("GUILDID")).split(" "))))
    async def _hero(self, interaction: Interaction, 
    hero_1: str = SlashOption(name="hero_1",description="Sphère du premier héro (Commandement,Connaissance,Energie,Tactique,Neutre...)", required=False,choices=["Aléatoire (par défaut)","Commandement","Tactique","Energie","Connaissance","Neutre","Sacquet","Communauté"]),
    hero_2: str = SlashOption(name="hero_2",description="Sphère du second héro (Commandement,Connaissance,Energie,Tactique,Neutre...)", required=False,choices=["Aléatoire (par défaut)","Commandement","Tactique","Energie","Connaissance","Neutre","Sacquet","Communauté","Pas de second héro"]),
    hero_3: str = SlashOption(name="hero_3",description="Sphère du troisème héro (Commandement,Connaissance,Energie,Tactique,Neutre...)", required=False,choices=["Aléatoire (par défaut)","Commandement","Tactique","Energie","Connaissance","Neutre","Sacquet","Communauté","Pas de troisième héro"])):
        print(f"{interaction.user} use Hero slash command" )
        #Retravaille des champs saisie par la commande
        hero_1 == share.hero_value(hero_1)
        hero_2 == share.hero_value(hero_2)
        hero_3 == share.hero_value(hero_3)
        list_cycle = ["Tout","Boîte de Base","Cycle 1 : Ombres de la Forêt Noire","Cycle 2 : Royaume de Cavenain","Cycle 3 : Face à l'Ombre","Cycle 4 : Le Créateur d'Anneaux","Cycle 5 : Le Réveil d'Angmar","Cycle 6 : Chasse-Rêve","Cycle 7 : Les Haradrim","Cycle 8 : Ered Mithrin","Cycle 9 : La Vengeance du Mordor","Extension de saga : Par Monts et par Souterrains","Extension de saga : Au Seuil de la Porte","Extension de saga : Les Cavaliers Noirs","Extension de saga : La Route s'Assombrit","Extension de saga : La Trahison de Saroumane","Extension de saga : La Terre de l'Ombre","Extension de saga : La Flamme de l'Ouest","Extension de saga : La Montagne de Feu","Starter pack : Les Nains de Durin","Starter pack : Les Elfes de la Lórien","Starter pack : Les Défenseurs du Gondor","Starter pack : Les Cavaliers du Rohan","A long Extented Party : Serment des Rohirrim"]
        view = SelectView(list_cycle,self.bot)
        await interaction.response.send_message(view=view,ephemeral=True)

def setup(bot):
    bot.add_cog(Hero(bot))