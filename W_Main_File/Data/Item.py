import abc
import random
from enum import Enum, IntFlag, auto
from typing import Union
import typing

if typing.TYPE_CHECKING:
    from W_Main_File.Data import HpEntity


class ItemType(Enum):
    Weapon = 3
    Armour = 5
    Consumable = 2
    Accessory = 4
    Quest = 1


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
    def __init__(self, name, id_, type_: ItemType, sprite):
        self.name = name
        self.id_ = id_
        self.type_ = type_
        self.sprite = sprite
        self.is_missingno = (id_ == 'MISSINGNO')
        self.selected = False

    def __repr__(self):
        return f'<{self.__class__.__name__} name = {self.name!r}, id = {self.id_!r}, type = {self.type_!r}>'


class Weapon(Item):
    def __init__(self, name, id_, min_attack, max_attack, speed, range_, damage_type: Union[int, DamageType], has_special_move: bool, sprite):
        super().__init__(name, id_, ItemType.Weapon, sprite)
        self.min_attack = min_attack
        self.max_attack = max_attack
        self.speed = speed
        self.range = range_
        self.damage_type = damage_type
        self.has_elemental_damage = bool(self.damage_type & DamageType.Any_Elemental)
        self.has_special_move = has_special_move

        """
        basic plated armour:
            16 physical def
            
        (enchanted) armour:
            12 physical def
            - attributes
                - fire resistance 30%
                - reflection 10%
        
        """

    def use_on_target(self, target: "HpEntity.HpEntity"):
        pass

    def use_special(self, target: "HpEntity.HpEntity"):
        pass

    def element_type(self):
        if self.has_elemental_damage:
            return self.damage_type & DamageType.Any_Elemental
        else:
            return DamageType.No

    def damage_inflicted(self, target: "HpEntity.HpEntity"):
        damage = random.randint(self.min_attack, self.max_attack)
        from W_Main_File.Utilities import Damage_Calc
        return Damage_Calc.calculate_damage(damage, self.damage_type, target)


class Armour(Item):
    """
    opposite of halfing is to double
    but opposite of -50% is +50%
    60 * .5
    60 / .5
    60 - (50% of 60)
    60 + (50% of 60)

    defense: 10
    vulnerable: 5
    strong: 15
    effects:
        EFFECT_DICT = {
            'stabby defense': def process(armour, effectiveness)
                              def does_apply(dmg_type) -> bool
        }
        - physical = 1
            - stabby = 2
            - slashy = 2
            - cutty = 2
            - ghosty = 2
            - nani = 2
        - magic
            - firey
            - watery
            - airy
            - voidy
            - earthy

        Incoming: 300 dmg, 200 stabby, 100 fire
        Armour: 10% stabby reduction, 50% fire reduction
        Resulting?: -30 from stabby, -150 from fire reduction
        Resulting?: -30 from stabby, -135 from fire reduction
        .15 .5 .30
        ZONED: default zone: GLOBAL
        Armour(..., attributes={'stabby defense': lambda x: x * .5, 'fire res': .3, default=lambda x: x * 1})

        100
        .3 res
        70
        - 5
        65

        100-5
        95
        .3

        5 / 0.7
        100-7.14..
        92.86

        attributes = {DamageType.VOID: 1.5}
        def apply_attibutes(total_dmg, dmg_types,


        max(res % applied to dmg - flat res, 1)

        Goblin {
            wearing:
                plated armor
            def res():
                {
                    FIRE: .5
                }
        }
    """

    def __init__(self, name, id_, level, defense, elemental_defense, max_durability, current_durability, attributes, sprite):
        super().__init__(name, id_, ItemType.Armour, sprite)
        self.min_attack = min_attack
        self.max_attack = max_attack
        self.speed = speed
        self.range = range_
        self.damage_type = damage_type
        self.has_elemental_damage = bool(self.damage_type & DamageType.Any_Elemental)
        self.has_special_move = has_special_move

    def use_on_target(self, target: "HpEntity.HpEntity"):
        pass

    def use_special(self, target: "HpEntity.HpEntity"):
        pass

    def element_type(self):
        if self.has_elemental_damage:
            return self.damage_type & DamageType.Any_Elemental
        else:
            return DamageType.No

    def damage_inflicted(self, target: "HpEntity.HpEntity"):
        damage = random.randint(self.min_attack, self.max_attack)
        from W_Main_File.Utilities import Damage_Calc
        return Damage_Calc.calculate_damage(damage, self.damage_type, target)
