from sqlalchemy import orm, exists, create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from sqlalchemy import func

engine = create_engine('sqlite:///Player_Saves.sqlite')
Base = declarative_base(bind=engine)
Session = orm.sessionmaker(bind=engine)


def init_tables():
    Base.metadata.create_all()


# noinspection PyUnresolvedReferences,PyBroadException
@contextmanager
def managed_session():
    con: Session = None
    try:
        con = orm.scoped_session(Session)
        yield con
    except Exception as _:
        import traceback
        traceback.print_exc()
    else:
        con.commit()
    finally:
        if con:
            con.close()


class PlayerData(Base):
    # noinspection SpellCheckingInspection
    __tablename__ = 'player_an_data_a'
    id = Column(Integer, primary_key=True, autoincrement=True)
    character_name = Column(String(15), nullable=False)
    character_pw = Column(String(50), nullable=False)
    player_x = Column(Integer, nullable=False, default=0)
    player_y = Column(Integer, nullable=False, default=0)
    hp = Column(Integer, nullable=False, default=200)
    max_hp = Column(Integer, nullable=False, default=220)
    gold = Column(Integer, nullable=False, default=0)
    xp = Column(Integer, nullable=False, default=0)
    lvl = Column(Integer, nullable=False, default=1)
    floor = Column(Integer, nullable=False, default=1)

    @classmethod
    def new(cls, name, pw, player_x=0, player_y=0, hp=200, max_hp=220, gold=0, xp=0, lvl=1, floor=1):
        return PlayerData(character_name=name, character_pw=pw, player_x=player_x, player_y=player_y, hp=hp, max_hp=max_hp, gold=gold, xp=xp, lvl=lvl, floor=floor)

    def as_dict(self):
        return dict(
            player_name=self.character_name,
            x=self.player_x,
            y=self.player_y,
            max_hp=self.max_hp,
            hp=self.hp,
            gold=self.gold,
            xp=self.xp,
            lvl=self.lvl,
            floor=self.floor
        )


init_tables()


def player_exists(session, name):
    return session.query(exists().where(func.lower(PlayerData.character_name) == name.lower())).scalar()


def get_player(session, name):
    return session.query(PlayerData).filter(func.lower(PlayerData.character_name) == name.lower()).one_or_none()


def load_player(session, name, pw):
    if player_exists(session, name):
        return get_player(session, name)
    player_info = PlayerData.new(name=name, pw=pw)
    session.add(player_info)
    return player_info


def load_and_validate_player(session, name, pw):
    player_info = load_player(session, name, pw)
    return player_info.character_pw == pw, player_info
