import json

class Guild:
    def __init__(self, id, prefix, emoji, mute_role, tmp_category):
        self.id = id
        self.prefix = prefix
        self.emoji = emoji
        self.mute_role = mute_role
        self.tmp_category = tmp_category

class GuildEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Guild):
            obj_dict = {key: str(obj.__dict__[key]) for key in obj.__dict__}
            return obj_dict

        return json.JSONEncoder.default(self, obj)