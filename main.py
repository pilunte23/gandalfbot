from http import client
import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import *
from dotenv import load_dotenv
from unidecode import unidecode
from function import *

load_dotenv(dotenv_path="config")

bot = commands.Bot(command_prefix='!', case_insensitive=True)
slash = SlashCommand(bot , sync_commands=True)

@bot.event
async def on_ready():
	""" check if bot is connected """
	print("Le robot est connecté comme {0.user}".format(bot))

initial_extensions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append("cogs." + filename[:-3])

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

bot.run(os.getenv("DISCORD_TOKEN"))