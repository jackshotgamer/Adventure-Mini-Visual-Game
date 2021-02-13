from sqlalchemy import orm, exists, create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

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
    player_x = Column(Integer, nullable=False, default=0)
    player_y = Column(Integer, nullable=False, default=0)
    hp = Column(Integer, nullable=False, default=100)
    max_hp = Column(Integer, nullable=False, default=120)
    gold = Column(Integer, nullable=False, default=0)
    xp = Column(Integer, nullable=False, default=0)
    lvl = Column(Integer, nullable=False, default=0)

    @classmethod
    def new(cls, name, player_x=0, player_y=0, hp=100, max_hp=120, gold=0, xp=0, lvl=0):
        return PlayerData(character_name=name.lower(), player_x=player_x, player_y=player_y, hp=hp, max_hp=max_hp, gold=gold, xp=xp, lvl=lvl)

    def as_dict(self):
        return dict(
            player_name=self.character_name,
            x=self.player_x,
            y=self.player_y,
            max_hp=self.max_hp,
            hp=self.hp,
            gold=self.gold,
            xp=self.xp,
            lvl=self.lvl
        )


init_tables()


def player_exists(session, name):
    return session.query(exists().where(PlayerData.character_name == name.lower())).scalar()


def get_player(session, name):
    return session.query(PlayerData).filter(PlayerData.character_name == name.lower()).one_or_none()


def load_player(session, name):
    if player_exists(session, name):
        return get_player(session, name)
    player_info = PlayerData.new(name=name)
    session.add(player_info)
    return player_info
