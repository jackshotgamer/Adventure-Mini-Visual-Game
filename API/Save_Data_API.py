import fastapi
from API import Database

app = fastapi.FastAPI()


@app.get('/save_data')
def get_save_file(name: str):
    with Database.managed_session() as session:
        player_data = Database.load_player(session, name.lower())
        return player_data.as_dict()


@app.post('/update')
def update_save_file(name, x: int = None, y: int = None, hp: int = None, gold: int = None, xp: int = None, lvl: int = None):
    with Database.managed_session() as session:
        if not Database.player_exists(session, name):
            return dict(
                error='Player does not exist!'
            )
        player_file = Database.load_player(session, name)

        for param in update_save_file.__code__.co_varnames:
            if param != 'name' and locals()[param] is not None:
                setattr(player_file, param, locals()[param])

        return dict(
            error=''
        )
