import os
import random

def get_random_image(path):
    return path + random.choice([x for x in os.listdir(path)
            if os.path.isfile(os.path.join(path, x))])