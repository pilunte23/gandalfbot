import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import *
from unidecode import unidecode
from PIL import Image
import json
import re
import os

class Player(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="c",
        description="Pour l'affichage de carte(s) joueur",
        guild_ids=list(map(int,str(os.getenv("GUILDID")).split(" "))),
        options=[
            create_option(
                name="recherche",
                description="Terme Recherché",
                required=True,
                option_type=3
            ),
            create_option(
                name="sphere",
                description="Filtre sur la Sphère (Commandement,Connaissance,Energie,Tactique,Neutre...)",
                required=False,
                option_type=3,
                choices=[
                    create_choice(
                        name="Pas de filtre (par défaut)",
                        value="all",        
                    ),
                    create_choice(    
                        name= "Commandement",
                        value="300"
                    ),
                    create_choice(
                        name="Connaissance",
                        value="303"
                    ),
                    create_choice(
                        name="Energie",
                        value="302"
                    ),
                    create_choice(
                        name="Tactique",
                        value="301"
                    ),
                    create_choice(
                        name="Neutre",
                        value="304"
                    ),
                    create_choice(
                        name="Communauté",
                        value="305"
                    ),
                    create_choice(
                        name="Sacquet",
                        value="306"
                    )
                ]
            ),
            create_option(
                name="type",
                description="Filtre sur le Type de Carte (Héro, Allié, Attachement, Evènement...)",
                required=False,
                option_type=3,
                choices=[
                    create_choice(
                        name="Pas de filtre (par défaut)",
                        value="all"
                    ),
                    create_choice(
                        name="Héro",
                        value="400"
                    ),
                    create_choice(
                        name="Allié",
                        value="401"
                    ),
                    create_choice(
                        name="Evènement",
                        value="402"
                    ),
                    create_choice(
                        name="Attachement",
                        value="403"
                    ),
                    create_choice(
                        name="Objectif Allié",
                        value="409"
                    ),
                    create_choice(
                        name="Trésor",
                        value="410"
                    ), 
                    create_choice(
                        name="Campagne",
                        value="411"
                    ),
                    create_choice(
                        name="Quête Annexe Joueur",
                        value="412"
                    ),
                    create_choice(
                        name="Navire Objectif",
                        value="411"
                    ),
                    create_choice(
                        name="Objectif Héros",
                        value="414"
                    ),                    
                    create_choice(
                        name="Contrat",
                        value="418"
                    )
                ]
            ),
            create_option(
                name="champs",
                description="Sur Quel Champs de Rechercher le Terme saisi (Nom, Traits , Illustrateur)",
                required=False,
                option_type=3,
                choices=[
                    create_choice(
                        name="Titre (par défaut)",
                        value="titre"
                    ),
                    create_choice(
                        name="Trait",
                        value="trait"
                    )
                ]
            ),
            create_option(
                name="selection",
                description="Type d'affichage (Liste Déroulante , Multicarte ou Liste)",
                required=False,
                option_type=3,
                choices=[
                    create_choice(
                        name="Renvoie une liste de carte via Menu sélectionnable limité à 25 cartes (par défaut)",
                        value="menu"
                    ),
                    create_choice(
                        name="Renvoie une image de plusieurs cartes limité à 10 cartes",
                        value="multicard"
                    )
                ]
            ),
            create_option(
                name="terme",
                description="Terme Exacte ou Partiel",
                required=False,
                option_type=3,
                choices=[
                    create_choice(
                        name="Terme partiel (par défaut)",
                        value="partial"
                    ),
                    create_choice(
                        name="Terme exact",
                        value="exact"
                    )
                ]
            )
        ]     
    )

    async def _carte(self,ctx, recherche:str,sphere="all",type= "all",selection="menu",champs="titre",terme="partial"):
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
        if terme =="exact":
            word_use = "^"+ unidecode(str(recherche.lower()))+"$"
        else:
            if champs == "trait":
                word_use = ".*\\b"+ unidecode(str(recherche.lower()))+"\\b.*"
            else:       
                word_use = ".*"+ unidecode(str(recherche.lower()))+".*"
        for i in data:
            all_search = None
            """ search in name, traits"""  
            if champs == "titre" and "titre" in i:
                all_search = re.search(word_use,unidecode(str(i["titre"].lower()))) 
            if champs == "trait" and "trait" in i:
                all_search = re.search(word_use,unidecode(str(i["trait"].lower())))
            if all_search:
                if ( sphere == i['id_sphere_influence'] or sphere == "all" ) and ( type == i['id_type_carte'] or type == "all" ):
                    """already_find = False  
                    for j in resultat_carte:
                            if i['titre'] == j['titre'] and i['id_sphere_influence'] == j['id_sphere_influence'] and i['texte'] == j['texte']:
                                already_find = True
                    if already_find == False:"""      
                    resultat_carte.append(i) 
      
        if len(resultat_carte) > 0:
            if len(resultat_carte) == 1:
                await sendcard(self,ctx,resultat_carte[0])
            else:
                if selection == "multicard":
                    if len(resultat_carte) > 10:
                        await _toomuchcard(self,ctx)
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
                        embed_carte = discord.Embed(name = "Test", color = discord.Color.blue())
                        file = discord.File("requête.png", filename = "image.png")
                        embed_carte.set_image(url ="attachment://image.png")
                        await ctx.send(file=file,embed = embed_carte)
                if selection == "menu": 
                    if len(resultat_carte) > 24:
                        await _toomuchcard(self,ctx)
                    else:
                        """menu for single card search"""
                        await _selectingbox(self,ctx,resultat_carte)       
               
        else:
            file_url = "./assets/picture/no_card.png"
            file = discord.File(file_url, filename="image.png")
            embed_no_carte = discord.Embed(name = "no result", color = discord.Color.red())
            embed_no_carte.set_image(url="attachment://image.png")
            embed_no_carte.add_field(name = "Aucune carte n'a été trouvée", value = "Vous ne passerez pas !!!")   
            await ctx.send(file=file,embed = embed_no_carte,delete_after= 5)


async def _toomuchcard(self,ctx):
    embed_too_carte = discord.Embed(name = "too much result", color = discord.Color.red())
    embed_too_carte.add_field(name = "Trop de résultat", value = "Veuillez affiner votre recherche")   
    await ctx.send(embed = embed_too_carte,delete_after= 5)


async def _selectingbox(self,ctx,resultat_carte):
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

    fait_ctx = await ctx.send("Choisissez votre carte", components=[create_actionrow(select)])

    def check(m):
        return m.author_id == ctx.author.id and m.origin_message.id == fait_ctx.id

    choice_ctx = await wait_for_component(self.bot,components=select, check=check)

    datacard = resultat_carte[int(choice_ctx.values[0])]
    await sendcard(self,ctx,datacard)
    await fait_ctx.delete()

async def sendcard(self,ctx,datacard):
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
        embed = discord.Embed(title=datacard['titre'],color=sphere_color)
    else:
        emoji = discord.utils.get(self.bot.emojis, name=sphere)
        embed = discord.Embed(title=f"{emoji} "+datacard['titre'],color=sphere_color)
    file = discord.File(file_url, filename="image.jpg")
    pack_file = discord.File(f"./assets/pack/{datacard['id_extension']}.png", filename="pack.png")
    embed.set_author(name=f"{datacard['lbl extension']}", url= f"https://sda.cgbuilder.fr/liste_carte/{datacard['id_extension']}/")
    embed.set_thumbnail(url=f"attachment://pack.png")
    embed.set_image(url="attachment://image.jpg")
    embed.set_footer(text=f"{cycle}")
    await ctx.send(files=[file,pack_file], embed=embed)


def setup(bot):
    bot.add_cog(Player(bot))