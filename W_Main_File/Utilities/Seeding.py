import random
import hashlib

world_seed = 1347825631267546181054095643186409
tile_rng = random.Random()


def vector_hasher(vector):
    return int(hashlib.md5(str((vector.x, vector.y)).encode()).hexdigest(), 16)


# noinspection PyShadowingNames
def seed_for_vector(world_seed, vector):
    vector_hash_number = vector_hasher(vector)
    current_seed = vector_hash_number + world_seed
    tile_rng.seed(current_seed)
    return tile_rng


def set_world_seed_from_string(text):
    global world_seed
    world_seed = int(hashlib.md5(text.encode()).hexdigest(), 16)


def change_world_seed(value):
    global world_seed
    world_seed = value
