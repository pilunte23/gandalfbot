import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import *
from unidecode import unidecode
from PIL import Image
import json
import re
import asyncio
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
                        value="leadership"
                    ),
                    create_choice(
                        name="Connaissance",
                        value="lore"
                    ),
                    create_choice(
                        name="Energie",
                        value="spirit"
                    ),
                    create_choice(
                        name="Tactique",
                        value="tactics"
                    ),
                    create_choice(
                        name="Neutre",
                        value="neutral"
                    ),
                    create_choice(
                        name="Sacquet",
                        value="baggins"
                    ),
                    create_choice(
                        name="Communauté",
                        value="fellowship"
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
                        value="Héro"
                    ),
                    create_choice(
                        name="Allié",
                        value="Allié"
                    ),
                    create_choice(
                        name="Attachement",
                        value="Attachement"
                    ),
                    create_choice(
                        name="Evènement",
                        value="Evènement"
                    ),
                    create_choice(
                        name="Contrat",
                        value="Contrat"
                    ),
                    create_choice(
                        name="Quête annexe",
                        value="Quête annexe"
                    ),
                    create_choice(
                        name="Campagne",
                        value="Campagne"
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
                        name="Nom (par défaut)",
                        value="name"
                    ),
                    create_choice(
                        name="Traits",
                        value="traits"
                    ),
                    create_choice(
                        name="Illustrateur",
                        value="illustrator"
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
                    ),
                    create_choice(
                        name="Renvoie une liste des cartes pour chaque sphère.",
                        value="list"
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

    async def _carte(self,ctx, recherche:str,sphere="all",type= "all",selection="menu",champs="name",terme="partial"):
        "pas de multilingue pour l'instant"
        langue="fr"
        resultat_carte = []
        img = []
        place = 0
        img_weight = 0
        url_file =  "./data/sda_"+langue+".json"
        f = open(url_file)
        data = json.load(f)

        if terme =="exact":
            word_use = "^"+ unidecode(str(recherche.lower()))+"$"
        else:
            if champs == "traits":
                word_use = ".*\\b"+ unidecode(str(recherche.lower()))+"\\b.*"
            else:       
                word_use = ".*"+ unidecode(str(recherche.lower()))+".*"
        for i in data:
            all_search = None
            """ search in name, traits, illustrator"""
            if champs == "name" and "name" in i:
                all_search = re.search(word_use,unidecode(str(i["name"].lower()))) 
            if champs == "traits" and "traits" in i:
                all_search = re.search(word_use,unidecode(str(i["traits"].lower())))
            if champs == "illustrator" and "illustrator" in i:
                all_search = re.search(word_use,unidecode(str(i["illustrator"].lower()))) 
            if all_search: 
                if ( sphere == i['sphere_code'] or sphere == "all" ) and ( type == i['type_name'] or type == "all" ):
                    """check exist octgn file"""
                    if "octgnid" in i:
                        """ remove (MotK) card and starter deck (no octgn file) and """
                        if not (re.search("(MotK)",i['name'])) and i['pack_code'] not in ["EoL", "DoG", "RoR", "DoD"] and not (re.search("ALeP",i['pack_name'])):
                            """ check if the id is already on the list """
                            already_find = False  
                            for j in resultat_carte:
                                if i['name'] == j['name'] and i['sphere_code'] == j['sphere_code'] \
                                and i['text'] == j['text']:
                                    already_find = True
                            if already_find == False:      
                                resultat_carte.append(i)                
        if len(resultat_carte) > 0:
            if len(resultat_carte) == 1:
                if langue == "fr": 
                    await sendcard(self,ctx,resultat_carte[0])
            else:
                if selection == "multicard":
                    if len(resultat_carte) > 10:
                        await _toomuchcard(self,ctx)
                    else:
                        """ define the size of the result with the number of card found """
                        img_weight = (img_weight + len(resultat_carte)) * 493
                        img_height = 700
                        """ add every patch in the list img """
                        for i in resultat_carte:
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
                if selection == "list":
                    await _listcard(self,ctx,resultat_carte,champs,recherche)                  
        else:
            file_url = "./assets/picture/no_card.png"
            file = discord.File(file_url, filename="image.png")
            embed_no_carte = discord.Embed(name = "no result", color = discord.Color.red())
            embed_no_carte.set_image(url="attachment://image.png")
            embed_no_carte.add_field(name = "Aucune carte n'a été trouvée", value = "Vous ne passerez pas !!!")   
            no_card_msg = await ctx.send(file=file,embed = embed_no_carte)
            await asyncio.sleep(5)
            await no_card_msg.delete()

async def _listcard(self,ctx,resultat_carte,champs,recherche):
    if champs == "name":
        lib_champs ="Nom"
    if champs == "traits":
        lib_champs ="Traits"   
    if champs == "illustrator":
        lib_champs ="Illustrateur"
    list_sphere={"leadership":[],"lore":[],"spirit":[],"tactics":[],"neutral":[],"baggins":[],"fellowship":[]}
    for i in resultat_carte:
        for j in list_sphere:
            if i['sphere_code'] == j:
                list_sphere[j].append(i)

    sphere_count = 0  
    for key,list_card in list_sphere.items():     
        if len(list_card) > 0:
            emoji = discord.utils.get(self.bot.emojis, name=key)
            count = 0 
            globals()[f"embed_list_card{sphere_count}"] = discord.Embed(title=f"Cartes {emoji} pour votre recherche par {lib_champs} : {recherche}", color = discord.Color.from_rgb(127, 64, 7))
            globals()[f"field{count}"] = ""
            for i in list_card:
                """if total file size < 1024"""
                if len(f"[{i['name']}]({i['url']})\n") + len(globals()[f"field{count}"]) < 1024:
                    globals()[f"field{count}"] = f"[{i['name']}]({i['url']}) {i['type_name']}\n" + globals()[f"field{count}"] 
                else:
                    """create new fields"""
                    globals()[f"embed_list_card{sphere_count}"].add_field(name = f"Carte(s) de la sphère {emoji}", value = globals()[f"field{count}"])  
                    count += 1
                    globals()[f"field{count}"] = ""            
                    globals()[f"field{count}"] = f"[{i['name']}]({i['url']}) {i['type_name']}\n" + globals()[f"field{count}"]
            globals()[f"embed_list_card{sphere_count}"].add_field(name = f"Carte(s) de la sphère {emoji}", value = globals()[f"field{count}"])  
            await ctx.send(embed = globals()[f"embed_list_card{sphere_count}"])
        sphere_count += 1
    
async def _toomuchcard(self,ctx):
    embed_too_carte = discord.Embed(name = "too much result", color = discord.Color.red())
    embed_too_carte.add_field(name = "Trop de résultat", value = "Veuillez affiner votre recherche")   
    too_card_msg = await ctx.send(embed = embed_too_carte)
    await asyncio.sleep(5)
    await too_card_msg.delete()

async def _selectingbox(self,ctx,resultat_carte):
    list_card = []
    count = 0
    for i in resultat_carte:
        if i['sphere_code'] == "spirit":
            altsphere_emoji = "🟦"
        if i['sphere_code'] == "lore":
            altsphere_emoji = "🟩"
        if i['sphere_code'] == "leadership":
            altsphere_emoji = "🟪"
        if i['sphere_code'] == "tactics":
            altsphere_emoji = "🟥"
        if i['sphere_code'] == "neutral":
            altsphere_emoji = "⬜"
        if i['sphere_code'] == "baggins":
            altsphere_emoji = "🟨"
        if i['sphere_code'] == "fellowship":
            altsphere_emoji = "🟧" 
        list_card.append(create_select_option(i['name']+" "+ i['type_name']+" "+ i['sphere_name'], value=str(count),emoji=altsphere_emoji))
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
    if datacard['sphere_code'] == "spirit":
        sphere_color = 0x33DDFF
    if datacard['sphere_code'] == "lore":
        sphere_color = 0x0E7A12
    if datacard['sphere_code'] == "leadership":
        sphere_color = 0x8B23F9
    if datacard['sphere_code'] == "tactics":
        sphere_color = 0xDB140B
    if datacard['sphere_code'] == "neutral":
        sphere_color = 0x797B7A
    if datacard['sphere_code'] == "baggins":
        sphere_color = 0xD3D911
    if datacard['sphere_code'] == "fellowship":
        sphere_color = 0xD99611
    cycle=""
    if datacard['pack_code'] in ["HfG","CatC","JtR","HoEM","TDM","RtM"]:
        cycle="Cycle 1 : Ombres de la Forêt Noire"
    if datacard['pack_code'] in ["KD","TRG","RtR","WitW","TLD","FoS","SaF"]:
        cycle="Cycle 2 : Royaume de Cavenain"
    if datacard['pack_code'] in ["HoN","AtS","TDF","EaAD","AoO","BoG","TMV"]:
        cycle="Cycle 3 : Face à l'Ombre"
    if datacard['pack_code'] in ["VoI","TDT","TTT","TiT","NiE","CS","TAC"]:
        cycle="Cycle 4 : Le Créateur d'Anneaux"
    if datacard['pack_code'] in ["TLR","WoE","EfMG","AtE","ToR","BoCD","TDR"]:
        cycle="Cycle 5 : Le Réveil d'Angmar"
    if datacard['pack_code'] in ["TGH","FotS","TitD","TotD","DR","SoCH","CoC"]:
        cycle="Cycle 6 : Chasse-Rêve"
    if datacard['pack_code'] in ["TSoH","M","RAH","BtS","TBS","DoCG","CoP"]:
        cycle="Cycle 7 : Les Haradrim"
    if datacard['pack_code'] in ["TWoR","TWH","RAR","FitN","TGoF","MG","TFoW"]:
        cycle="Cycle 8 : Ered Mithrin"
    if datacard['pack_code'] in ["ASitE","WaR","TCoU","CotW","UtAM","TLoS","TFoN"]:
        cycle="Cycle 9 : La Vengeance du Mordor"
    if datacard['pack_code'] == "OHaUH":
        cycle="Extension de saga : Par Monts et par Souterrains"
    if datacard['pack_code'] == "OtD":
        cycle="Extension de saga : Au Seuil de la Porte"
    if datacard['pack_code'] == "TBR":
        cycle="Extension de saga : Les Cavaliers Noirs"
    if datacard['pack_code'] == "TRD":
        cycle="Extension de saga : La Route s'Assombrit"
    if datacard['pack_code'] == "ToS":
        cycle="Extension de saga : La Trahison de Saroumane"
    if datacard['pack_code'] == "LoS":
        cycle="Extension de saga : La Terre de l'Ombre"
    if datacard['pack_code'] == "FotW":
        cycle="Extension de saga : La Flamme de l'Ouest"
    if datacard['pack_code'] == "MoF":
        cycle="Extension de saga : La Montagne de Feu"

    file_url = "./images/"+datacard['octgnid']+".jpg"
    emoji = discord.utils.get(self.bot.emojis, name=datacard['sphere_code'])
    embed = discord.Embed(title=f"{emoji} "+datacard['name'],color=sphere_color)
    file = discord.File(file_url, filename="image.jpg")
    pack_file = discord.File(f"./assets/pack/{datacard['pack_code']}.png", filename="pack.png")
    embed.set_author(name=f"{datacard['pack_name']}", url= f"https://ringsdb.com/set/{datacard['pack_code']}")
    if datacard['has_errata']:
        errata=f"Cette carte possède une [FAQ](http://lotr-lcg-quest-companion.gamersdungeon.net/#Card{datacard['position']})"
        embed.add_field(name="\u200b",value=errata) #creates embed
    embed.set_thumbnail(url=f"attachment://pack.png")
    embed.set_image(url="attachment://image.jpg")
    embed.set_footer(text=f"{cycle}")
    await ctx.send(files=[file,pack_file], embed=embed)

def setup(bot):
    bot.add_cog(Player(bot))