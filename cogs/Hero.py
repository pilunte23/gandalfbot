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
    def __init__(self):
        selectoptions = []
        list_cycle =[]
        url_file =  "./data/SDA_carte_joueur.json"
        f =  open(url_file , encoding="utf8")
        rawdata = json.load(f)
        for i in rawdata:
            card_cycle = share.info_cycle(i)
            if card_cycle not in list_cycle:
                list_cycle.append(card_cycle)
                selectoptions.append(SelectOption(label=card_cycle,description="",value=card_cycle))
        print(str(len(selectoptions)))
        print(str(list_cycle))
        super().__init__(placeholder="Quelle cycle possedez vous? ",min_values=1,max_values=len(selectoptions) ,options=selectoptions)
        
    async def callback(self,interaction: Interaction):
        selected_list= self.values
        return await interaction.message(str(selected_list))
    
class SelectView(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(myselect())

class Hero(commands.Cog):

    def __init__(self, bot):
        self.bot:  commands.bot = bot

    @nextcord.slash_command(name="h",description="Tirage des Héros aléatoires",guild_ids=list(map(int,str(os.getenv("GUILDID")).split(" "))))
    async def _hero(self, interaction: Interaction, 
    hero_1: str = SlashOption(name="hero_1",description="Sphère du premier héro (Commandement,Connaissance,Energie,Tactique,Neutre...)", required=False,choices=["Aléatoire (par défaut)","Commandement","Tactique","Energie","Connaissance","Neutre","Sacquet","Communauté"]),
    hero_2: str = SlashOption(name="hero_2",description="Sphère du second héro (Commandement,Connaissance,Energie,Tactique,Neutre...)", required=False,choices=["Aléatoire (par défaut)","Commandement","Tactique","Energie","Connaissance","Neutre","Sacquet","Communauté","Pas de second héro"]),
    hero_3: str = SlashOption(name="hero_3",description="Sphère du troisème héro (Commandement,Connaissance,Energie,Tactique,Neutre...)", required=False,choices=["Aléatoire (par défaut)","Commandement","Tactique","Energie","Connaissance","Neutre","Sacquet","Communauté","Pas de troisième héro"])):

        #Retravaille des champs saisie par la commande
        hero_1 == share.hero_value(hero_1)
        hero_2 == share.hero_value(hero_2)
        hero_3 == share.hero_value(hero_3)

        view = SelectView()
        await interaction.response.send_message(view=view,ephemeral=True)

def setup(bot):
    bot.add_cog(Hero(bot))

"""

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
                if i["pack_code"] not in ["EoL", "DoG", "RoR", "DoD", "Starter" ]:
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

 
        img_weight = (img_weight + len(resultat_carte)) * 493
        img_height = 700

        for i in resultat_carte:
            img.append(i['octgnid']+".jpg")

        new_img = Image.new('RGB', (img_weight, img_height), (250,250,250))

        for i in img:
            image = Image.open("./images/"+i)
            largeur = 0+(place*493)
            new_img.paste(image, (largeur, 0))
            place += 1

        new_img.save("requête.png", "PNG")

        embed_carte = Embed(name = "Test", color = nextcord.Color.blue())
        file = File("requête.png", filename = "image.png")
        embed_carte.set_image(url ="attachment://image.png")
        await ctx.send(file=file,embed = embed_carte)
                  
"""