import nextcord 
from nextcord.ext import commands
from nextcord import Interaction
import os
from typing import Optional, Set
from nextcord import Embed



class mymodal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Profile"
    )
        
        self.main_title = nextcord.ui.TextInput(
            label="Name"
        )

        self.add_item(self.main_title)

    async def callback(self, interaction: Interaction):
        title = self.main_title.value
        return await interaction.send(f"Titre: {title}")

class Modal(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="Test l'affichage d'une modal",guild_ids=list(map(int,str(os.getenv("GUILDID")).split(" "))))
    async def modal(self, interaction : nextcord.Interaction):
        modal = mymodal()
        await interaction.response.send_modal(modal=modal)
        

def setup(bot):
    bot.add_cog(Modal(bot))