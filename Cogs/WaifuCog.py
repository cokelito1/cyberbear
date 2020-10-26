import discord
from discord.ext import commands
from discord.ext.commands import Cog

from context import Context

from helper import get_random_image

context = Context()

class Waifus(Cog):
    """Commands related to waifus"""

    @commands.command(pass_context=True, brief='Envia una waifu al canal', description="Selecciona una waifu de la carpeta waifus en el directorio que se ejecuto el bot")
    async def waifu(self, ctx):
        context.new_guild_check(ctx.guild.id)

        if ctx.channel.is_nsfw():
            await ctx.send(file=discord.File(get_random_image("./waifus/")))
            await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)
        else:
            await ctx.send('Solo se puede usar en canales nsfw')
            await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)

    @commands.command(pass_context=True, brief="Envia una foto de futaba al canal", description="Selecciona una imagen de futaba de la carpeta futaba especificamente para memineitor")
    async def futaba(self, ctx):
        context.new_guild_check(ctx.guild.id)
        await ctx.send(file=discord.File(get_random_image("./futaba/")))
        await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)

    @commands.command(pass_context=True, brief="Envia una foto de mai al canal", description="Selecciona una imagen de mai de la carpeta futaba especificamente para mai")
    async def mai(self, ctx):
        context.new_guild_check(ctx.guild.id)
        await ctx.send(file=discord.File(get_random_image("./mai/")))
        await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)
