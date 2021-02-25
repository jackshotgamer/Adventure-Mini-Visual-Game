import requests
import State
from urllib.parse import quote


server_address = 'http://localhost:666/{}'


def save():
    player = State.state.player
    r = requests.post(server_address.format(f'update?name={quote(State.state.player.name)}&pw={State.state.pw}&player_x={player.pos.x}&player_y={player.pos.y}&xp={player.xp}'
                                            f'&hp={player.hp}&gold={player.gold}&lvl={player.lvl}&floor={player.floor}&max_hp={player.max_hp}'))
    print(f'name={quote(State.state.player.name)}&pw={State.state.pw}&x={player.pos.x}&y={player.pos.y}&xp={player.xp}'
          f'&hp={player.hp}&gold={player.gold}&lvl={player.lvl}&floor={player.floor}&max_hp={player.max_hp}')
    r_ = requests.get(server_address.format(f'save_data?name={quote(State.state.player.name)}&pw={State.state.pw}'))
    print(r_.json())
