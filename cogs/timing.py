import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import *
import os

class Timing(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name="t",
        description="Affiche le timing des phases du jeu",
        #guild_ids=list(map(int,str(os.getenv("GUILDID")).split(" "))),
        options=[create_option(
            name="timing",
            description="Affiche le timing des phases du jeu",
            option_type=3,
            required=True,
            choices=[
                        create_choice(
                            name="Phases",
                            value="phases"
                        ),
                        create_choice(
                            name="Combat",
                            value="combat"
                        )
                    ]
        )                    
        ]
    )

    async def _timing(self,ctx,timing):  
        file_url = f"./assets/timing/{timing}.png"
        file = discord.File(file_url, filename="image.png")
        embed_no_carte = discord.Embed(name = f"{timing}", color = discord.Color.red())
        embed_no_carte.set_image(url="attachment://image.png")  
        await ctx.send(file=file,embed = embed_no_carte)

def setup(bot):
    bot.add_cog(Timing(bot))