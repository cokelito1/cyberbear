import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord.utils import get

from context import Context

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

    @commands.command(pass_context=True, brief="mute", description="mute person")
    async def mute(self, ctx, user: discord.Member):
        context.new_guild_check(ctx.guild.id)

        if ctx.message.author.guild_permissions.administrator:
            if context.guilds[ctx.guild.id].mute_role != -1:
                mute_r = get(ctx.guild.roles, id=context.guilds[ctx.guild.id].mute_role)

                await user.add_roles(mute_r)
                await ctx.send("se muteo a " + str(user))
                await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)
            else:
                await ctx.send("Ocupe el comand set_mute_role para poner el rol de muteo")
                await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)
        else:
            await ctx.send("Solo lo puede ocupar un administrador")
            await ctx.message.add_reaction(context.guilds[ctx.guild.id].emoji)