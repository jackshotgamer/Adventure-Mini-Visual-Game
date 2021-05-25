

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

    @property
    def resistances(self):
        from W_Main_File.Data.Item import DamageType
        return {
            DamageType.Blunt: 1,
            DamageType.Piercing: 1,
            DamageType.Cutting: 1,
            DamageType.Water_Elemental: 1,
            DamageType.Earth_Elemental: 1,
            DamageType.Fire_Elemental: 1,
            DamageType.Air_Elemental: 1,
        }
