from W_Main_File.Data import Meta_Data
from W_Main_File.Utilities import Vector
from W_Main_File.Data.Item import DamageType

"""
for equipped_item in Entity.equipped_items:
    for attribute in equipped_item.attributes:
        Entity.resistances[attribute[0]] += attribute[1]
"""


class HpEntity:
    def __init__(self, name, pos, max_hp, hp, gold, lvl, meta_data=None, ):
        self.name = name
        self.pos = pos
        self.max_hp = max_hp
        self.hp = hp
        self.gold = gold
        self.lvl = lvl
        if meta_data:
            self.meta_data = meta_data
        else:
            self.meta_data = Meta_Data.MetaData()
        from W_Main_File.Items.Inventory import InventoryContainer
        self.inventory = InventoryContainer()
        self.resistance_dict = {
            DamageType.Blunt: 1,
            DamageType.Piercing: 1,
            DamageType.Cutting: 1,
            DamageType.Water_Elemental: 1,
            DamageType.Earth_Elemental: 1,
            DamageType.Fire_Elemental: 1,
            DamageType.Air_Elemental: 1,
        }

    @property
    def resistances(self):
        return self.resistance_dict


class PlayerEntity(HpEntity):
    def __init__(self, name, pos, max_hp, hp, gold, xp, lvl, floor, meta_data: Meta_Data.MetaData = None, deaths=0, realm='Overworld'):
        if not meta_data:
            meta_data = Meta_Data.MetaData(is_player=True)
        super().__init__(name, pos, max_hp, hp, gold, lvl, meta_data)
        self.xp = xp
        self.floor = floor
        self.deaths = deaths
        self.realm = realm
        self.camera_pos = Vector.Vector(0, 0)


class NPCEntity(HpEntity):
    def __init__(self, name, pos, max_hp, hp, gold, xp, lvl, floor, realm='Overworld'):
        super().__init__(name, pos, max_hp, hp, gold, lvl)
        self.xp = xp
        self.floor = floor
        self.realm = realm


class EnemyEntity(HpEntity):
    def __init__(self, name, pos, species, max_hp, hp, gold, lvl):
        super().__init__(name, pos, max_hp, hp, gold, lvl)
        self.species = species
        from W_Main_File.Data import Attributes
        self.attributes = Attributes.AttributeSupervisor()


class SpecialEnemyEntity(HpEntity):
    def __init__(self, name, pos, species, max_hp, hp, gold, lvl, floor, realm='Overworld'):
        super().__init__(name, pos, max_hp, hp, gold, lvl)
        self.species = species
        self.floor = floor
        self.realm = realm
