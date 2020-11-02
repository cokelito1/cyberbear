import os
import random
import json

from waifu import WaifuData
from context import Context

ctx = Context()

def get_random_image(path):
    return path + random.choice([x for x in os.listdir(path)
            if os.path.isfile(os.path.join(path, x))])

def get_random_waifu_data():
    return random.choice(list(ctx.waifus.values()))