import discord
from discord.ext import commands
from discord.ext.commands import Cog

from context import Context

from helper import get_random_image
from helper import get_random_waifu_data

import numpy as np

def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    return (matrix[size_x - 1, size_y - 1])

context = Context()

def closestKey(data, val):
    lastKey = None
    lastDif = 9999
    for key in sorted(data.keys()):
        dif = levenshtein(key, val) #need to figure out difference()
        if lastDif > dif and dif < 5:
            lastDif = dif
            lastKey = key

    return lastKey

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

        if name == "":
            waifu = get_random_waifu_data()
            emb = discord.Embed(title="Tu nueva waifu", color=0x00ff00)
            emb.add_field(name="Nombre", value=waifu.name, inline=False)
            emb.add_field(name="Serie", value=waifu.serie, inline=False)
            emb.set_image(url=waifu.url)

            await ctx.send(embed=emb)
            await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)
        else:
            key = closestKey(context.waifus, name)
            if key == None:
                await ctx.send("no se encontro una waifu con ese nombre")
                await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)
            else:
                waifu = context.waifus[closestKey(context.waifus, name)]
                emb = discord.Embed(title="Tu nueva waifu", color=0x00ff00)
                emb.add_field(name="Nombre", value=waifu.name, inline=False)
                emb.add_field(name="Serie", value=waifu.serie, inline=False)
                emb.set_image(url=waifu.url)

                await ctx.send(embed=emb)
                await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)


