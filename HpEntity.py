

class HpEntity:
    def __init__(self, name, pos, max_hp, hp, gold, xp, lvl, floor, meta_data=None):
        self.name = name
        self.pos = pos
        self.max_hp = max_hp
        self.hp = hp
        self.gold = gold
        self.xp = xp
        self.lvl = lvl
        self.floor = floor
        self.meta_data = meta_data
