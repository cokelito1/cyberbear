import discord
from discord.ext import commands
from discord.ext.commands import Cog

from context import Context

context = Context()

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