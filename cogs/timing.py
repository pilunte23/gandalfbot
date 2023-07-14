import nextcord 
from nextcord.ext import commands
from nextcord import Interaction
import os

class Timing(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="t",description="Affiche le timing des phases du jeu",guild_ids=list(map(int,str(os.getenv("GUILDID")).split(" "))))
    async def _timing(self, interaction: Interaction, timing: str = nextcord.SlashOption(name="timing", choices=["phases", "combat"])):
        print(f"{interaction.user} use Timing slash command" )
        file_url = f"./assets/timing/{timing}.png"
        file = nextcord.File(file_url, filename="image.png")
        embed_no_carte = nextcord.Embed(title = f"{timing}", color = nextcord.Color.red())
        embed_no_carte.set_image(url="attachment://image.png")  
        await interaction.send(file=file,embed = embed_no_carte)

def setup(bot):
    bot.add_cog(Timing(bot))