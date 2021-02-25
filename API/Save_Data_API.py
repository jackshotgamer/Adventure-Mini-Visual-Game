import fastapi
from API import Database

app = fastapi.FastAPI()


@app.get('/save_data')
def get_save_file(name: str, pw: str):
    with Database.managed_session() as session:
        password_valid, player_data = Database.load_and_validate_player(session, name, pw)
        if not password_valid:
            return dict(
                error='Password Incorrect'
            )
        return {**player_data.as_dict(), 'error': ''}


@app.post('/update')
def update_save_file(name: str, pw: str, player_x: int = None, player_y: int = None, hp: int = None, gold: int = None, xp: int = None, lvl: int = None, floor: int = None):
    with Database.managed_session() as session:
        if not Database.player_exists(session, name):
            return dict(
                error='Player does not exist!'
            )
        password_valid, player_file = Database.load_and_validate_player(session, name, pw)
        if not password_valid:
            return dict(
                error='Password Incorrect'
            )

        for param in update_save_file.__code__.co_varnames:
            if param != 'name' and locals()[param] is not None:
                if param != 'pw':
                    setattr(player_file, param, locals()[param])

        return dict(
            error=''
        )
