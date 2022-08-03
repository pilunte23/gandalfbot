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
        url_file =  "./data/pack.json"
        f = open(url_file)
        dataPack = json.load(f)
        randomPack = random.randint(0, len(dataPack)-1)
        pack_name= dataPack[randomPack]['code']

        url_file =  "./data/sda_fr.json"
        f = open(url_file)
        dataCard = json.load(f)
        for i in dataCard:
            if i["pack_code"] == pack_name:
                resultat_carte.append(i)

        randomCard = random.randint(0, len(resultat_carte)-1) 
        await sendcard(self,ctx,resultat_carte[randomCard])
                    
async def sendcard(self,ctx,datacard):

    #channel = discord.utils.get(ctx.guild.channels, name="carte-du-jour")
    channel = self.bot.get_channel("984083665028014130")
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
    bot.add_cog(Random(bot))