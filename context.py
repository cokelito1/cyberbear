from guild import Guild
from guild import GuildEncoder

import json

default_emoji = '\N{White Heavy Check Mark}'

default_prefixes = ['cb.']

class Context:
    def __init__(self):
        self.guilds = {}

        with open('guilds.json', 'r') as f:
            tmp_guilds = json.load(f)
            for key in tmp_guilds:
                self.guilds[int(key)] = Guild(tmp_guilds[key]["id"], tmp_guilds[key]["prefix"], tmp_guilds[key]["emoji"])
                print(int(key), self.guilds[int(key)].id, self.guilds[int(key)].prefix, self.guilds[int(key)].emoji)

    def check_guild(self, guild_id):
        return guild_id in self.guilds

    def new_guild_check(self, guild_id):
        if not self.check_guild(guild_id):
            self.guilds[guild_id] = Guild(guild_id, 'cb.', default_emoji)

    def save(self):
        file = 'guilds.json'
        with open(file, 'w') as f:
            json.dump(self.guilds, f, cls=GuildEncoder, indent=4)

    async def determine_prefix(self, bot, message):
        guild = message.guild
        if guild:
            self.new_guild_check(guild.id)
            return [self.guilds.get(guild.id).prefix]
        else:
            return default_prefixes

