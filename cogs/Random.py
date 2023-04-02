import os
import nextcord 
from nextcord.ext import commands
from nextcord import Interaction
import json
import random
import share 

class Random(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name="a",description="Carte Aleatoire",guild_ids=list(map(int,str(os.getenv("GUILDID")).split(" "))))
 
    async def _cardoftheday(self,interaction: Interaction):
        resultat_carte=[]   
        url_file =  "./data/SDA_carte_joueur.json"
        f =  open(url_file , encoding="utf8")
        dataCard = json.load(f)
        for i in dataCard:
            #exclusion les Two-Player Limited Edition et les éditions révisées
            #exclusion allié-héros
            #garde uniquement les cartes joueurs
            if i['id_extension'] not in ['67','82', '83', '84', '85','87', '88', '91', '94'] and "&bull" not in i['titre'] and i['id_type_carte'] in ['400','401','402','403']:
                resultat_carte.append(i)

        randomCard = random.randint(0, len(resultat_carte)-1) 
        await sendcard(self,interaction,resultat_carte[randomCard])
                    
async def sendcard(self,interaction,datacard):

    """ beautiful embed """
    sphere, sphere_color=share.info_sphere(datacard)
    cycle=share.info_cycle(datacard)
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
    bot.add_cog(Random(bot))