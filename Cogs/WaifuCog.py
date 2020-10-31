import discord
from discord.ext import commands
from discord.ext.commands import Cog

from context import Context

from helper import get_random_image
from helper import get_random_waifu_data

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

    @commands.command(pass_context=True)
    async def discover_waifu(self, ctx, name=""):
        context.new_guild_check(ctx.guild.id)
        waifu = get_random_waifu_data()
        emb = discord.Embed(title="Tu nueva waifu", color=0x00ff00)
        emb.add_field(name="Nombre", value=waifu.name, inline=False)
        emb.add_field(name="Serie", value=waifu.serie, inline=False)
        emb.set_image(url=waifu.url)

        await ctx.send(embed=emb)
        await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)
