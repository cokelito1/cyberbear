import discord
from discord.ext import commands

import os
import random
import json

from guild import Guild
from guild import GuildEncoder

token = os.getenv('CYBER_BEAR_TOKEN')
default_emoji = '\N{White Heavy Check Mark}'

if token == None:
    print("Pls set CYBER_BEAR_TOKEN to the bot token")
    exit(0)

custom_prefixes = {}
default_prefixes = ['cb.']

guilds = {}

tmp_channels = []
tmp_roles = []

def check_guild(guild_id):
    return guild_id in guilds

def new_guild_check(guild_id):
    if not check_guild(guild_id):
        guilds[guild_id] = Guild(guild_id, 'cb.', default_emoji)

def get_random_image(path):
    return path + random.choice([x for x in os.listdir(path)
               if os.path.isfile(os.path.join(path, x))])

async def determine_prefix(bot, message):
    guild = message.guild
    if guild:
        new_guild_check(guild.id)
        return [guilds.get(guild.id).prefix]
    else:
        return default_prefixes

bot = commands.Bot(command_prefix=determine_prefix)

@bot.command()
async def echo(ctx, wea):
    await ctx.send(wea)

@bot.command(brief='Crear canal temporal', description='cb.cc <nombre_canal> @persona_1 @persona_2...')
async def cc(ctx, channel_name):
    new_guild_check(ctx.guild.id)

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

        tmp_channels.append(ch)
        tmp_roles.append(c)

        await ctx.message.add_reaction(guilds[ctx.guild.id].emoji)

    except Exception as e:
        print("error " + str(e))

@bot.command(brief='Borrar canales temporales sin gente', description='cb.prune <Opt<nombre canal>>')
async def prune(ctx, name = ""):
    new_guild_check(ctx.guild.id)

    if name != "":
        for i in tmp_roles:
            if i.name == '<tmp> ' + name:
                await i.delete()

        for i in tmp_channels:
            if i.name == '<tmp> ' + name:
                await i.delete()
        
        await ctx.message.add_reaction(guilds[ctx.guild.id].emoji)
        print("Pruned {}".format(name))       
        return
    
    for z in ctx.guild.categories:
        if z.name == "Temporales":
            for i in z.channels:
                if len(i.members) == 0:
                    for j in tmp_roles:
                        if j.name == i.name:
                            await j.delete()
                            tmp_roles.remove(j)
                    await i.delete()
                    tmp_channels.remove(i)
           

    await ctx.message.add_reaction(guilds[ctx.guild.id].emoji)
    print("pruned")

@bot.command(brief='cb.image', description='Imagen random de la carpeta del basti')
async def image(ctx):
    new_guild_check(ctx.guild.id)

    await ctx.send(file=discord.File(get_random_image("./images/")))
    await ctx.message.add_reaction(guilds[ctx.guild.id].emoji)

@bot.command(brief="cb.waifu", description='Una waifu para todos')
async def waifu(ctx):
    new_guild_check(ctx.guild.id)

    if ctx.channel.is_nsfw():
        await ctx.send(file=discord.File(get_random_image("./waifus/")))
        await ctx.message.add_reaction(guilds[ctx.guild.id].emoji)
    else:
        await ctx.send('Solo se puede usar en canales nsfw')
        await ctx.message.add_reaction(guilds[ctx.guild.id].emoji)

@bot.command(brief="cb.futaba", description="Una futaba para memineitor")
async def futaba(ctx):
    new_guild_check(ctx.guild.id)
    await ctx.send(file=discord.File(get_random_image("./futaba/")))
    await ctx.message.add_reaction(guilds[ctx.guild.id].emoji)

@bot.command(brief="cb.mai", description="Una mai para memineitor")
async def mai(ctx):
    new_guild_check(ctx.guild.id)
    await ctx.send(file=discord.File(get_random_image("./mai/")))
    await ctx.message.add_reaction(guilds[ctx.guild.id].emoji)

def save():
    file = 'guilds.json'
    with open(file, 'w') as f:
        json.dump(guilds, f, cls=GuildEncoder, indent=4)

@bot.command()
async def set_prefix(ctx, prefix=""):
    new_guild_check(ctx.guild.id)

    if ctx.message.author.guild_permissions.administrator:
        guilds[ctx.guild.id].prefix = prefix
        save()
        await ctx.send("El prefix ahora es " + guilds[ctx.guild.id].prefix)
        await ctx.message.add_reaction(guilds[ctx.guild.id].emoji)
    else:
        await ctx.send("Solo lo puede ocupar un administrador")
        await ctx.message.add_reaction(guilds[ctx.guild.id].emoji)

@bot.command()
async def set_emoji(ctx, emo: discord.PartialEmoji):
    new_guild_check(ctx.guild.id)

    if ctx.message.author.guild_permissions.administrator:
        if emo.is_custom_emoji():
            guilds[ctx.guild.id].emoji = str(emo)
            await ctx.send("El nuevo emoji es " + str(guilds[ctx.guild.id].emoji))
            await ctx.message.add_reaction(guilds[ctx.guild.id].emoji)
            save()
    else:
        await ctx.send("Solo lo puede ocupar un administrador")
        await ctx.message.add_reaction(guilds[ctx.guild.id].emoji)

@bot.command()
async def print_guilds(ctx):
    print(guilds)

with open('guilds.json', 'r') as f:
    tmp_guilds = json.load(f)
    for key in tmp_guilds:
        guilds[int(key)] = Guild(tmp_guilds[key]["id"], tmp_guilds[key]["prefix"], tmp_guilds[key]["emoji"])
        print(int(key), guilds[int(key)].id, guilds[int(key)].prefix, guilds[int(key)].emoji)

print('Starting bot with token {}'.format(token))
bot.run(token)