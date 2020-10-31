import os
import random
import json

from waifu import WaifuData

def get_random_image(path):
    return path + random.choice([x for x in os.listdir(path)
            if os.path.isfile(os.path.join(path, x))])

def get_random_waifu_data():
    with open(get_random_image("./waifus_data/")) as f:
        tmp_data = json.load(f)
        return WaifuData(tmp_data["nombre"], tmp_data["serie"], tmp_data["image_url"])