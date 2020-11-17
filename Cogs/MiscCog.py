import discord
from discord.ext import commands
from discord.ext.commands import Cog

from context import Context

from helper import get_random_image

import time

context = Context()

class Misc(Cog):
    """Miscelanneous commands"""

    @commands.command(pass_context="True", brief="una imagen random", description="Una imagen random de la carpeta del basti")
    async def image(self, ctx):
        context.new_guild_check(ctx.guild.id)

        await ctx.send(file=discord.File(get_random_image("./images/")))
        await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)

    @commands.command(pass_context="True")
    async def memineitor(self, ctx):
        context.new_guild_check(ctx.guild.id)

        await ctx.send(file=discord.File(get_random_image("./memineitor/")))
        await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)

    @commands.command(pass_context="True")
    async def play(self, ctx):
        context.new_guild_check(ctx.guild.id)

        await ctx.send(file=discord.File(get_random_image("./plays/")))
        await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)

    @commands.command(pass_context="True", brief="Envia una imagen al server")
    async def send_image(self, ctx):
        context.new_guild_check(ctx.guild.id)

        i = 0
        timestr = time.strftime("%Y%m%d-%H%M%S")
        for img in ctx.message.attachments:
            try:
                with open("./images/" + ctx.author.name + "_" + str(i) + "_" + timestr + "_" + img.filename, "wb") as f:
                    await img.save(f)
                    print("se guardo " + "./images/" + ctx.author.name + "_" + str(i) + "_" + timestr + "_" + img.filename)
            except:
                await ctx.send("Hubo un error al guardar imagen")
                await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)

            i = i + 1

        await ctx.send("Se guardaron las imagenes")
        await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)
