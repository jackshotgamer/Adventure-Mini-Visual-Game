import random
import hashlib

from W_Main_File.Essentials import State

world_seed = -1
tile_rng = random.Random()


def vector_hasher(vector):
    return int(hashlib.md5(str((vector.x, vector.y)).encode()).hexdigest(), 16)


# noinspection PyShadowingNames
def seed_for_vector(vector):
    vector_hash_number = vector_hasher(vector)
    current_seed = vector_hash_number + get_floor_seed()
    tile_rng.seed(current_seed)
    return tile_rng


def set_world_seed_from_player_name():
    global world_seed
    world_seed = int(hashlib.md5(State.state.player.name.encode()).hexdigest(), 16)


def get_floor_seed():
    return world_seed + State.state.player.floor
