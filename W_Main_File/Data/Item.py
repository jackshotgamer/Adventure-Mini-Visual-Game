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
    No = 0
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

    # Armour
        # Water: Increase HP
            # Set: Heal 1 hp for every 5 damage dealt
        # Earth: Increase Percentage Damage Reduction
            # Set: Take no damage every third hit
        # Fire: Increase Debuff Reduction
            # Set: Deal DOT fire damage
        # Air: Increase Evasion
            # Set: Increase movement speed based on proximity to enemies, up to x2.5
        # Void: All four
            # Set: twice per fight, unleash a wave of damage that does your maximum damage to all enemies,
            # halves their movement speed for 15 seconds, and gives them DOT 5% health every second for 5 seconds, makes you invulnerable for 3 seconds,
            # and gives you 25% health back over 15 seconds
    # Weapons
        # Water:

    Any_Elemental = Water_Elemental | Earth_Elemental | Fire_Elemental | Air_Elemental | Void_Elemental
    Any_Basic = Blunt | Piercing | Cutting | Spectral | Null

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
        self.is_missingno = (id_ == 'MISSINGNO')

    def __repr__(self):
        return f'<{self.__class__.__name__} name = {self.name!r}, id = {self.id_!r}, type = {self.type_!r}>'


class Weapon(Item):
    def __init__(self, name, id_, min_attack, max_attack, speed, range_, damage_type: Union[int, DamageType], has_special_move: bool):
        super().__init__(name, id_, ItemType.Weapon)
        self.min_attack = min_attack
        self.max_attack = max_attack
        self.speed = speed
        self.range = range_
        self.damage_type = damage_type
        self.has_elemental_damage = bool(self.damage_type & DamageType.Any_Elemental)
        self.has_special_move = has_special_move

    def use_on_target(self, target: HpEntity.HpEntity):
        pass

    def use_special(self, target: HpEntity.HpEntity):
        pass

    def element_type(self):
        if self.has_elemental_damage:
            return self.damage_type & DamageType.Any_Elemental
        else:
            return DamageType.No

    def damage_inflicted(self, target: HpEntity):
        damage = random.randint(self.min_attack, self.max_attack)
        from W_Main_File.Utilities import Damage_Calc
        return Damage_Calc.calculate_damage(damage, self.damage_type, target)
