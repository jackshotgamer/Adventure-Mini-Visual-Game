import abc
import random
from enum import Enum, IntFlag, auto
from typing import Union

from W_Main_File.Data import HpEntity, Sprites_


class ItemType(Enum):
    Weapon = 1
    Armour = 2
    Consumable = 3
    Accessory = 4


class DamageType(IntFlag):
    Blunt = auto()
    Piercing = auto()
    Cutting = auto()
    Spectral = auto()
    Null = auto()
    Water_Elemental = auto()
    Earth_Elemental = auto()
    Fire_Elemental = auto()
    Air_Elemental = auto()
    Void_Elemental = auto()

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
    def __init__(self, name, id_, type_: ItemType, sprite=Sprites_.Null):
        self.name = name
        self.id_ = id_
        self.type_ = type_
        self.sprite = sprite
        self.is_missingno = (id_ == 'MISSINGNO')

    def __repr__(self):
        return f'<{self.__class__.__name__} name = {self.name!r}, id = {self.id_!r}, type = {self.type_!r}>'


class Weapon(Item):
    def __init__(self, name, id_, min_attack, max_attack, speed, damage_type: Union[int, DamageType], has_special_move: bool, sprite=Sprites_.Null):
        super().__init__(name, id_, ItemType.Weapon, sprite=sprite)
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
        from W_Main_File.Utilities import Damage_Calc
        return Damage_Calc.calculate_damage(damage, self.damage_type, target)
