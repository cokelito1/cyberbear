import discord
from discord.ext import commands
from discord.ext.commands import Cog

import os
import random
import json

from guild import Guild
from guild import GuildEncoder

from context import Context

token = os.getenv('CYBER_BEAR_TOKEN')

if token == None:
    print("Pls set CYBER_BEAR_TOKEN to the bot token")
    exit(0)

context = Context()

def get_random_image(path):
    return path + random.choice([x for x in os.listdir(path)
               if os.path.isfile(os.path.join(path, x))])

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

class Canales(Cog):
    """Commands related to channels"""

    @commands.command(pass_context=True, brief="Crear un canal temporal", description="poner el nombre del canal y mencionar a la gente")
    async def cc(self, ctx, channel_name):
        context.new_guild_check(ctx.guild.id)

        try:
            name = '<tmp> ' + channel_name

            category = ctx.guild.categories[-1]

            c = await ctx.guild.create_role(name=name)

            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                ctx.guild.me: discord.PermissionOverwrite(view_channel=True),
                c: discord.PermissionOverwrite(view_channel=True)
            }

            ch = await ctx.guild.create_voice_channel(name, overwrites=overwrites, category=category)
            
            for i in ctx.message.mentions:
                await i.add_roles(c)

            await ctx.message.author.add_roles(c)
            await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)

        except Exception as e:
            print("error " + str(e))

    @commands.command(pass_context=True, brief="Borrar canales temporales no usados", description="Borra los canales temporales que no estan siendo utilizados en el momento")
    async def prune(self, ctx, name = ""):
        context.new_guild_check(ctx.guild.id)

        if name != "":
            for i in tmp_roles:
                if i.name == '<tmp> ' + name:
                    await i.delete()

            for i in tmp_channels:
                if i.name == '<tmp> ' + name:
                    await i.delete()
            
            await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)
            print("Pruned {}".format(name))       
            return
        
        for z in ctx.guild.categories:
            if z.name == "Temporales":
                for i in z.channels:
                    if len(i.members) == 0:
                        for j in ctx.message.guild.roles:
                            if j.name == i.name:
                                await j.delete()
                        await i.delete()
            

        await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)
        print("pruned")

    @commands.command(pass_context=True, brief="Agregar al rol temporal", description="Agregar personas al rol de un canal temporal")
    async def add(self, ctx):
        if ctx.message.author.voice != None:
            if ctx.message.author.voice.channel != None:
                if ctx.message.author.voice.channel.category != None:
                    if ctx.message.author.voice.channel.category.name == "Temporales":
                        role = ctx.message.guild.roles[0]
                        for a in ctx.message.guild.roles:
                            if a.name == ctx.message.author.voice.channel.name:
                                role = a
                        for i in ctx.message.mentions:        
                                    await i.add_roles(role)

                        await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)
                    else:
                        await ctx.send("Este canal debe pertenecer a la categoria de Temporales")
                        await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)
                else:
                    await ctx.send("Este canal debe pertenecer a la categoria de Temporales")
                    await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)
            else:
                await ctx.send("Necesitas estar conectado a un canal de voz para ocupar este comando")
                await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji) 
        else:
            await ctx.send("Necesitas estar conectado a un canal de voz para ocupar este comando")
            await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)

class Misc(Cog):
    """Miscelanneous commands"""

    @commands.command(pass_context="True", brief="una imagen random", description="Una imagen random de la carpeta del basti")
    async def image(self, ctx):
        context.new_guild_check(ctx.guild.id)

        await ctx.send(file=discord.File(get_random_image("./images/")))
        await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)


bot = commands.Bot(command_prefix=context.determine_prefix)
bot.add_cog(Waifus())
bot.add_cog(Administration())
bot.add_cog(Canales())
bot.add_cog(Misc())

print('Starting bot with token {}'.format(token))
bot.run(token)