import nextcord 
from nextcord.ext import commands
from nextcord import Interaction, SelectOption, ui, SlashOption, Embed, File
from unidecode import unidecode
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
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
    
    async def callback(self,interaction: Interaction ):

        resultat_carte=[]
        selected_list_id = share.id_extension_by_cycle_name(self.values)
        url_file =  "./data/SDA_carte_joueur.json"
        f =  open(url_file , encoding="utf8")
        rawdata = json.load(f)

        heros1 = []
        heros2 = []
        heros3 = []
        
        for i in rawdata:
            if i['id_extension'] in selected_list_id and i['id_type_carte']=="400" and i["id_sphere_influence"] not in ["305","306"] and "&bull" not in i['titre']:
                heros1.append(i)                        
                heros2.append(i)              
                heros3.append(i)
        if heros1 != []:       
            randomHero1 = random.randint(0, len(heros1)-1)
            resultat_carte.append(heros1[randomHero1])
        if heros2 != []:       
            randomHero2 = random.randint(0, len(heros2)-1)
            while heros1[randomHero1]["titre"] == heros2[randomHero2]["titre"]:
                randomHero2 = random.randint(0, len(heros2)-1)
            resultat_carte.append(heros2[randomHero2])
        if heros3 != []:       
            randomHero3 = random.randint(0, len(heros3)-1)
            while heros1[randomHero1]["titre"] == heros3[randomHero3]["titre"] or heros2[randomHero2]["titre"] == heros3[randomHero3]["titre"]:
                randomHero3 = random.randint(0, len(heros3)-1) 
            resultat_carte.append(heros3[randomHero3])
        

        url_file =  "./data/SDA_carte_quete.json"
        f =  open(url_file , encoding="utf8")
        rawdata = json.load(f)
        scenarios = []
        for i in rawdata:
            if i['id_extension'] in selected_list_id and i['lbl set rencontre'] not in scenarios:
                scenarios.append(i)
        randomValue = random.randint(0, len(scenarios)-1)
        randomScenario= scenarios[randomValue]
        scenario = randomScenario['lbl set rencontre']
        cycle = share.info_cycle(randomScenario,"long")
        print(scenario)
        print(cycle)
        """font = ImageFont.load_default()
        img_scenario = Image.open("assets/picture/scenario.png")
        draw = ImageDraw.Draw(img_scenario)
        draw.text((394, 560),text,font=font, fill="white")
        img_scenario.save("scenario.png")"""
        # Open an Image
        img_scenario = Image.open("assets/picture/scenario.png")
        #Pour linux
        font = ImageFont.load_default()
        font2 = ImageFont.load_default()
        #Pour windows
        #font = ImageFont.truetype("times-ro.ttf", 28, encoding="unic")
        #font2 = ImageFont.truetype("times-ro.ttf", 14, encoding="unic")
        # Call draw Method to add 2D graphics in an image
        I1 = ImageDraw.Draw(img_scenario)
        W, H =  (394 , 560)
        _, _, w, h = I1.textbbox((0, 0), scenario, font=font)
        I1.text(((W-w)/2, (H-h)/2), scenario, font=font, fill="white")
        I1.text(((W-w)/6, (H-h)/6), cycle, font=font2, fill="white")
        # Display edited image
        #img_scenario.show()
 
        # Save the edited image
        img_scenario.save("scenario.png")


        img = []
        place = 0
        img_weight = len(resultat_carte) * 394 + 788
        img_height = 560
        """ add every patch in the list img """
        for i in resultat_carte:   
                src_file="sda_cgbuilder/images/simulateur/carte/"+i['id_extension']+"/"+i['numero_identification']+".jpg"
                img.append(src_file)
        img.append("assets/picture/vs_complete.png")
        img.append('scenario.png')

        """ creating the new img who will be send """
        new_img = Image.new('RGB', (img_weight, img_height), (250,250,250))
        """ we paste every image in the new_img """
        for i in img:
            image = Image.open("./"+i)
            largeur = 0+(place*394)
            new_img.paste(image, (largeur, 0))
            place += 1
        """ saving the result in a png """
        new_img.save("defi.png", "PNG")
        """ beautiful embed """
        embed_carte = Embed(title = "Défi aléatoires")
        file = File("defi.png", filename = "image.png")
        embed_carte.set_image(url ="attachment://image.png")
        return await interaction.send(files=[file], embed=embed_carte)
    
class SelectView(ui.View):
    def __init__(self,list_cycle,bot):
        super().__init__()
        self.bot = bot
        self.add_item(myselect(list_cycle,bot))

class Defi(commands.Cog):

    def __init__(self, bot):
        self.bot:  commands.bot = bot

    @nextcord.slash_command(name="defi",description="Tirage de Héros et d'un scénario aléatoire avec votre collection du Seigneur des anneaux JCE",guild_ids=list(map(int,str(os.getenv("GUILDID")).split(" "))))
    async def _hero(self, interaction: Interaction):
        print(f"{interaction.user} use Defi slash command" )
        #Retravaille des champs saisie par la commande
        list_cycle = ["Tout","Boîte de Base","Cycle 1 : Ombres de la Forêt Noire","Cycle 2 : Royaume de Cavenain","Cycle 3 : Face à l'Ombre","Cycle 4 : Le Créateur d'Anneaux","Cycle 5 : Le Réveil d'Angmar","Cycle 6 : Chasse-Rêve","Cycle 7 : Les Haradrim","Cycle 8 : Ered Mithrin","Cycle 9 : La Vengeance du Mordor","Extension de saga : Par Monts et par Souterrains","Extension de saga : Au Seuil de la Porte","Extension de saga : Les Cavaliers Noirs","Extension de saga : La Route s'Assombrit","Extension de saga : La Trahison de Saroumane","Extension de saga : La Terre de l'Ombre","Extension de saga : La Flamme de l'Ouest","Extension de saga : La Montagne de Feu","Starter pack : Les Nains de Durin","Starter pack : Les Elfes de la Lórien","Starter pack : Les Défenseurs du Gondor","Starter pack : Les Cavaliers du Rohan","A long Extented Party : Serment des Rohirrim"]
        view = SelectView(list_cycle,self.bot)
        await interaction.response.send_message(view=view,ephemeral=True)

def setup(bot):
    bot.add_cog(Defi(bot))