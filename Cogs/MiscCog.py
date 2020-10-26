import discord
from discord.ext import commands
from discord.ext.commands import Cog

from context import Context

from helper import get_random_image

context = Context()

class Misc(Cog):
    """Miscelanneous commands"""

    @commands.command(pass_context="True", brief="una imagen random", description="Una imagen random de la carpeta del basti")
    async def image(self, ctx):
        context.new_guild_check(ctx.guild.id)

        await ctx.send(file=discord.File(get_random_image("./images/")))
        await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)