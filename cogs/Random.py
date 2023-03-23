import discord
import os
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_components import *
import json
import random

class Random(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="a",
        description="Carte Aleatoire",
        guild_ids=list(map(int,str(os.getenv("GUILDID")).split(" ")))         
    )
#    @commands.Cog.listener()
#    async def on_ready(self):
#        """ check if bot is connected """
#        print("Le robot est connecté comme {0.user}".format(self.bot))
#        await cardoftheday(self)

    async def _cardoftheday(self,ctx):
        resultat_carte=[]   
        url_file =  "./data/SDA_carte_joueur.json"
        f =  open(url_file , encoding="utf8")
        dataCard = json.load(f)
        for i in dataCard:
            #exclusion les Two-Player Limited Edition et les éditions révisées
            #exclusion allié-héros
            #garde uniquement les cartes joueurs
            if i['id_extension'] not in ['67', '87', '82', '83', '84', '88', '91', '92'] and "&bull" not in i['titre'] and i['id_type_carte'] in ['400','401','402','403']:
                resultat_carte.append(i)

        randomCard = random.randint(0, len(resultat_carte)-1) 
        await sendcard(self,ctx,resultat_carte[randomCard])
                    
async def sendcard(self,ctx,datacard):

    #channel = discord.utils.get(ctx.guild.channels, name="carte-du-jour")
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
    pack_file = discord.File(f"./sda_cgbuilder/images/extension/{datacard['id_extension']}.png", filename="pack.png")
    embed.set_author(name=f"Nom du pack", url= f"https://sda.cgbuilder.fr/liste_carte/{datacard['id_extension']}/")
    embed.set_thumbnail(url=f"attachment://pack.png")
    embed.set_image(url="attachment://image.jpg")
    embed.set_footer(text=f"{cycle}")
    await ctx.send(files=[file,pack_file], embed=embed)


def setup(bot):
    bot.add_cog(Random(bot))