import requests
from W_Main_File.Essentials import State
from urllib.parse import quote


server_address = 'http://localhost:666/{}'


def save():
    player = State.state.player
    r = requests.post(server_address.format(f'update?name={quote(State.state.player.name)}&pw={State.state.pw}&player_x={player.pos.x}&player_y={player.pos.y}&xp={player.xp}'
                                            f'&hp={player.hp}&gold={player.gold}&lvl={player.lvl}&floor={player.floor}&max_hp={player.max_hp}&deaths={player.deaths}'))
