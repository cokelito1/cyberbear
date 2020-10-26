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

token = os.getenv('CYBER_BEAR_TOKEN')

if token == None:
    print("Pls set CYBER_BEAR_TOKEN to the bot token")
    exit(0)

context = Context()

class Administration(Cog):
    """Commands related to administration"""

    @commands.command(pass_context=True, brief="Seleccionar el prefijo para el servidor", description="Cambia el prefijo para el servidor permanentemente")
    async def set_prefix(self, ctx, prefix=""):
        context.new_guild_check(ctx.guild.id)

        if ctx.message.author.guild_permissions.administrator:
            context.guilds[ctx.guild.id].prefix = prefix
            context.save()
            await ctx.send("El prefix ahora es " + context.guilds[ctx.guild.id].prefix)
            await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)
        else:
            await ctx.send("Solo lo puede ocupar un administrador")
            await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)

    @commands.command(pass_context=True, brief="Cambia el emoji con el que reacciona el bot", description="Cambia el emoji con el que reacciona el bot permanentemente")
    async def set_emoji(self, ctx, emo: discord.PartialEmoji):
        context.new_guild_check(ctx.guild.id)

        if ctx.message.author.guild_permissions.administrator:
            if emo.is_custom_emoji():
                context.guilds[ctx.guild.id].emoji = str(emo)
                await ctx.send("El nuevo emoji es " + str(context.guilds[ctx.guild.id].emoji))
                await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)
                context.save()
        else:
            await ctx.send("Solo lo puede ocupar un administrador")
            await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)


bot = commands.Bot(command_prefix=context.determine_prefix)
bot.add_cog(Waifus())
bot.add_cog(Administration())
bot.add_cog(Canales())
bot.add_cog(Misc())

print('Starting bot with token {}'.format(token))
bot.run(token)