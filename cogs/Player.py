import nextcord 
from nextcord.ext import commands
from nextcord import Interaction
from unidecode import unidecode
from PIL import Image
import json
import re
import os

class Player(commands.Cog):

    def __init__(self, bot):
        self.bot:  commands.bot = bot

    @nextcord.slash_command(name="c",description="Pour l'affichage de carte(s) joueur",guild_ids=list(map(int,str(os.getenv("GUILDID")).split(" "))))
    async def _timing(self, 
    interaction: Interaction, 
    recherche: str = nextcord.SlashOption(name="recherche",description="Terme Recherché", required=True),
    type: str = nextcord.SlashOption(name="type",description="Filtre sur le Type de Carte (Héro, Allié, Attachement, Evènement...)",required=False,choices=["Pas de filtre (par défaut)","Héro","Allié","Evènement","Attachement","Objectif Allié","Trésor","Quête Annexe Joueur","Navire Objectif","Objectif Héros","Contrat"]),
    sphere: str = nextcord.SlashOption(name="sphere",description="Filtre sur la Sphère (Commandement,Connaissance,Energie,Tactique,Neutre...)",required=False,choices=["Pas de filtre (par défaut)","commandement","tactique","énergie","connaissance","neutre","Sacquet","communauté"]),
    champs: str = nextcord.SlashOption(name="champs",description="Sur Quel Champs de Rechercher le Terme saisi (Nom, Traits)",required=False, choices=["Titre (par défaut)", "Trait"]),  
    selection: str = nextcord.SlashOption(name="selection",description="Type d'affichage (Liste Déroulante ou Multicarte)",required=False, choices=["Renvoie une liste de carte via Menu sélectionnable limité à 25 cartes (par défaut)", "Renvoie une image de plusieurs cartes limité à 10 cartes"]),
    terme: str = nextcord.SlashOption(name="terme",description="Terme Exacte ou Partiel",required=False, choices=["Terme partiel (par défaut)", "Terme exact"])                                        
    ):
        if type == None or type =="Pas de filtre (par défaut)": type = "all"
        if sphere == None or sphere == "Pas de filtre (par défaut)": sphere = "all"
        if champs == None: champs ="Titre (par défaut)"
        if selection == None: selection ="Renvoie une liste de carte via Menu sélectionnable limité à 25 cartes (par défaut)"
        if terme == None: terme ="Terme partiel (par défaut)"
        
        print ("sphere:"+ sphere +" type:"+ type +" selection:"+ selection +" champs:"+ champs +" terme:"+ terme)
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
        if terme =="Terme exact":
            word_use = "^"+ unidecode(str(recherche.lower()))+"$"
        else:
            if champs == "Trait":
                word_use = ".*\\b"+ unidecode(str(recherche.lower()))+"\\b.*"
            else:       
                word_use = ".*"+ unidecode(str(recherche.lower()))+".*"
        for i in data:
            row_search = None
            """ search in name, traits"""  
            if champs == "Titre (par défaut)" and "titre" in i:
                row_search = re.search(word_use,unidecode(str(i["titre"].lower()))) 
            if champs == "Trait" and "trait" in i:
                row_search = re.search(word_use,unidecode(str(i["trait"].lower())))
            if row_search:
                if ( sphere == i['id_sphere_influence'] or sphere == "all" ) and ( type == i['id_type_carte'] or type == "all" ):   
                    resultat_carte.append(i) 
      
        if len(resultat_carte) > 0:
            if len(resultat_carte) == 1:
                await sendcard(self,interaction,resultat_carte[0])
            else:
                if selection == "multicard":
                    if len(resultat_carte) > 10:
                        await _toomuchcard(self,interaction)
                    else:
                        """ define the size of the result with the number of card found """
                        img_weight = (img_weight + len(resultat_carte)) * 394
                        img_height = 560
                        """ add every patch in the list img """
                        for i in resultat_carte:
                            img.append("sda_cgbuilder/images/simulateur/carte/"+i['id_extension']+"/"+i['numero_identification']+".jpg")
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
                        embed_carte = nextcord.Embed(titre = "Test", color = nextcord.Color.blue())
                        file = nextcord.File("requête.png", filename = "image.png")
                        embed_carte.set_image(url ="attachment://image.png")
                        await interaction.send(file=file,embed = embed_carte)
                if selection == "menu": 
                    if len(resultat_carte) > 24:
                        await _toomuchcard(self,interaction)
                    else:
                        """menu for single card search"""
                        await _selectingbox(self,interaction,resultat_carte)       
               
        else:
            file_url = "./assets/picture/no_card.png"
            file = nextcord.File(file_url, filename="image.png")
            embed_no_carte = nextcord.Embed(title = "no result", color = nextcord.Color.red())
            embed_no_carte.set_image(url="attachment://image.png")
            embed_no_carte.add_field(name = "Aucune carte n'a été trouvée", value = "Vous ne passerez pas !!!")   
            await interaction.send(file=file,embed = embed_no_carte,delete_after= 5)


async def _toomuchcard(self,interaction):
    embed_too_carte = nextcord.Embed(title = "too much result", color = nextcord.Color.red())
    embed_too_carte.add_field(name = "Trop de résultat", value = "Veuillez affiner votre recherche")   
    await interaction.send(embed = embed_too_carte,delete_after= 5)


async def _selectingbox(self,interaction,resultat_carte):
    selectOptions

    """
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
            
        list_card.append(create_select_option(i['titre']+" "+ i['lbl sphere influence'], value=str(count),emoji=altsphere_emoji))
        count += 1
        select = create_select(
        options=list_card,
        placeholder="choix de la carte",
        min_values=1,
        max_values=1
        )  
      

    fait_ctx = await interaction.send("Choisissez votre carte", components=[create_actionrow(select)])

    def check(m):
        return m.author_id == interaction.author.id and m.origin_message.id == fait_ctx.id

    choice_ctx = await wait_for_component(self.bot,components=select, check=check)

    datacard = resultat_carte[int(choice_ctx.values[0])]
    await sendcard(self,interaction,datacard)
    await fait_ctx.delete()
    """

async def sendcard(self,interaction,datacard):
    """ beautiful embed """
    sphere=""
    sphere_color = 0xFFFFFF
    if datacard['id_sphere_influence'] == "300":
        sphere_color = 0x8B23F9
        sphere="leadership"
    if datacard['id_sphere_influence'] == "301":
        sphere_color = 0x0E7A12
        sphere="lore"
    if datacard['id_sphere_influence'] == "302":
        sphere_color = 0x33DDFF
        sphere="spirit"
    if datacard['id_sphere_influence'] == "303":
        sphere_color = 0xDB140B
        sphere="tactics"
    if datacard['id_sphere_influence'] == "304":
        sphere_color = 0x797B7A
        sphere="neutral"
    if datacard['id_sphere_influence'] == "305":
        sphere_color = 0xD99611
        sphere="fellowship"
    if datacard['id_sphere_influence'] == "306":
        sphere_color = 0xD3D911
        sphere="baggins"
    cycle=""
    if datacard['id_extension'] in ['2', '3', '4', '5', '6', '7']:
        cycle="Cycle 1 : Ombres de la Forêt Noire"
    if datacard['id_extension'] in ['8', '9', '10', '11', '12', '13', '14']:
        cycle="Cycle 2 : Royaume de Cavenain"
    if datacard['id_extension'] in ['15', '16', '17', '18', '19', '20', '21']:
        cycle="Cycle 3 : Face à l'Ombre"
    if datacard['id_extension'] in ['22', '23', '24', '25', '26', '27', '28']:
        cycle="Cycle 4 : Le Créateur d'Anneaux"
    if datacard['id_extension'] in ['29', '30', '31', '32', '33', '34', '35']:
        cycle="Cycle 5 : Le Réveil d'Angmar"
    if datacard['id_extension'] in ['36', '37', '38', '39', '40', '41', '42']:
        cycle="Cycle 6 : Chasse-Rêve"
    if datacard['id_extension'] in ['50', '51', '52', '53', '54', '55', '56']:
        cycle="Cycle 7 : Les Haradrim"
    if datacard['id_extension'] in ['65', '66', '68', '69', '70', '71', '72']:
        cycle="Cycle 8 : Ered Mithrin"
    if datacard['id_extension'] in ['73', '74', '75', '76', '77', '78', '79']:
        cycle="Cycle 9 : La Vengeance du Mordor"
    if datacard['id_extension'] == "43":
        cycle="Extension de saga : Par Monts et par Souterrains"
    if datacard['id_extension'] == "44":
        cycle="Extension de saga : Au Seuil de la Porte"
    if datacard['id_extension'] == "45":
        cycle="Extension de saga : Les Cavaliers Noirs"
    if datacard['id_extension'] == "46":
        cycle="Extension de saga : La Route s'Assombrit"
    if datacard['id_extension'] == "47":
        cycle="Extension de saga : La Trahison de Saroumane"
    if datacard['id_extension'] == "48":
        cycle="Extension de saga : La Terre de l'Ombre"
    if datacard['id_extension'] == "49":
        cycle="Extension de saga : La Flamme de l'Ouest"
    if datacard['id_extension'] == "57":
        cycle="Extension de saga : La Montagne de Feu"

    file_url = "./sda_cgbuilder/images/simulateur/carte/"+datacard['id_extension']+"/"+ datacard['numero_identification']+".jpg"
    if sphere == "":
        embed = nextcord.Embed(title=datacard['titre'],color=sphere_color)
    else:
        emoji = nextcord.utils.get(self.bot.emojis, name=sphere)
        embed = nextcord.Embed(title=f"{emoji} "+datacard['titre'],color=sphere_color)
    file = nextcord.File(file_url, filename="image.jpg")
    pack_file = nextcord.File(f"./assets/pack/{datacard['id_extension']}.png", filename="pack.png")
    embed.set_author(name=f"{datacard['lbl extension']}", url= f"https://sda.cgbuilder.fr/liste_carte/{datacard['id_extension']}/")
    embed.set_thumbnail(url=f"attachment://pack.png")
    embed.set_image(url="attachment://image.jpg")
    embed.set_footer(text=f"{cycle}")
    await interaction.send(files=[file,pack_file], embed=embed)


def setup(bot):
    bot.add_cog(Player(bot))