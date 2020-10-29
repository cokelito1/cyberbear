from guild import Guild
from guild import GuildEncoder

import json
import os.path
from os import path

default_emoji = '\N{White Heavy Check Mark}'

default_prefixes = ['cb.']

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Context(metaclass=SingletonMeta):
    def __init__(self):
        self.guilds = {}

        if path.exists("guilds.json"):
            with open('guilds.json', 'r') as f:
                tmp_guilds = json.load(f)
                for key in tmp_guilds:
                    t_id = key
                    t_prefix = "cb."
                    t_emoji = default_emoji
                    t_mute_role = -1

                    if "id" in tmp_guilds[key]:
                        t_id = tmp_guilds[key]["id"]

                    if "prefix" in tmp_guilds[key]:
                        t_prefix = tmp_guilds[key]["prefix"]

                    if "emoji" in tmp_guilds[key]:
                        t_emoji = tmp_guilds[key]["emoji"]
                    
                    if "mute_role" in tmp_guilds[key]:
                        t_mute_role = int(tmp_guilds[key]["mute_role"])

                    self.guilds[int(key)] = Guild(t_id, t_prefix, t_emoji, t_mute_role)
                    print(int(key), self.guilds[int(key)].id, self.guilds[int(key)].prefix, self.guilds[int(key)].emoji, self.guilds[int(key)].mute_role)

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

