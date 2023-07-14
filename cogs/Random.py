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
        print(f"{interaction.user} use Random slash command" )
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
        await share.sendcard(self,interaction,resultat_carte[randomCard]) 
                    
def setup(bot):
    bot.add_cog(Random(bot))