from http import client
import os
import nextcord
from discord.ext import commands
from dotenv import load_dotenv
from function import *

load_dotenv(dotenv_path="config")

bot = commands.Bot(command_prefix='!', case_insensitive=True)
#slash = SlashCommand(bot , sync_commands=True)

initial_extensions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append("cogs." + filename[:-3])

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

bot.run(os.getenv("DISCORD_TOKEN"))