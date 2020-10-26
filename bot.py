import discord
from discord.ext import commands
from discord.ext.commands import Cog

import os
import random
import json

from guild import Guild
from guild import GuildEncoder

from context import Context
from helper import get_random_image

from Cogs.WaifuCog import Waifus
from Cogs.MiscCog import Misc
from Cogs.CanalesCog import Canales
from Cogs.AdministrationCog import Administration

token = os.getenv('CYBER_BEAR_TOKEN')

if token == None:
    print("Pls set CYBER_BEAR_TOKEN to the bot token")
    exit(0)

context = Context()

bot = commands.Bot(command_prefix=context.determine_prefix)
bot.add_cog(Waifus())
bot.add_cog(Administration())
bot.add_cog(Canales())
bot.add_cog(Misc())

print('Starting bot with token {}'.format(token))
bot.run(token)