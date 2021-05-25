from enum import Enum, IntFlag, auto
import abc, random

from W_Main_File.Data import HpEntity
from W_Main_File.Essentials import State


class ItemType(Enum):
    Weapon = 1
    Armour = 2
    Consumable = 3
    Accessory = 4


class DamageType(IntFlag):
    Blunt = auto()
    Piercing = auto()
    Cutting = auto()

    Water_Elemental = auto()
    Earth_Elemental = auto()
    Fire_Elemental = auto()
    Air_Elemental = auto()

    Any_Elemental = Water_Elemental | Earth_Elemental | Fire_Elemental | Air_Elemental
    Any_Basic = Blunt | Piercing | Cutting

    # blunt 0b1
    # Piercing 0b11
    # Cutting 0b111
    # Any_Elemental = 1111000
    # 0b0001000
    # &  101000
    #      1000
    # 1001000 & 1111000 == 1111000 = False


class Item:
    def __init__(self, name, id_, type_: ItemType):
        self.name = name
        self.id_ = id_
        self.type_ = type_


class Weapon(Item, metaclass=abc.ABCMeta):
    def __init__(self, name, id_, min_attack, max_attack, speed, damage_type: DamageType, has_special_move: bool):
        super().__init__(name, id_, ItemType.Weapon)
        self.min_attack = min_attack
        self.max_attack = max_attack
        self.speed = speed
        self.damage_type = damage_type
        self.has_elemental_damage = bool(self.damage_type & DamageType.Any_Elemental)
        self.has_special_move = has_special_move

    def use_on_target(self, target: HpEntity.HpEntity):
        pass

    def use_special(self, target: HpEntity.HpEntity):
        pass

    def damage_inflicted(self, target: HpEntity):
        damage = random.randint(self.min_attack, self.max_attack)
        if self.has_elemental_damage:
            elemental_damage = damage * 0.2
        else:
            elemental_damage = 0
        resistances = target.resistances
        total_damage = (damage * resistances[self.damage_type & DamageType.Any_Basic]) + (elemental_damage * resistances[self.damage_type & DamageType.Any_Elemental])
        return int(total_damage)
