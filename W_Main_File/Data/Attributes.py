# from W_Main_File.Data.Item import DamageType
from enum import Enum, IntFlag, auto


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

    def __repr__(self):
        return self.name


class AttributeSupervisor:
    def __init__(self):
        self.applied_attributes = {}
        self._resistances = {
            DamageType.No: 0,
            DamageType.Blunt: 1,
            DamageType.Piercing: 1,
            DamageType.Cutting: 1,
            DamageType.Spectral: 1,
            DamageType.Null: 1,
            DamageType.Water_Elemental: 1,
            DamageType.Earth_Elemental: 1,
            DamageType.Fire_Elemental: 1,
            DamageType.Air_Elemental: 1,
            DamageType.Void_Elemental: 1,
        }

    def reset_resistances(self):
        self._resistances = {
            DamageType.No: 0,
            DamageType.Blunt: 1,
            DamageType.Piercing: 1,
            DamageType.Cutting: 1,
            DamageType.Spectral: 1,
            DamageType.Null: 1,
            DamageType.Water_Elemental: 1,
            DamageType.Earth_Elemental: 1,
            DamageType.Fire_Elemental: 1,
            DamageType.Air_Elemental: 1,
            DamageType.Void_Elemental: 1,
        }

    @property
    def resistances(self):
        return self._resistances.copy()

    def apply(self, damage: dict):
        total_damage = 0
        for damage_type, damage in damage.items():
            total_damage += (self._resistances[damage_type] * damage)
        return total_damage

    def set(self, r_type, value, origin: str = None):
        if origin is not None:
            self.applied_attributes[origin] = ['set', r_type, value, self._resistances[r_type]]
        self._resistances[r_type] = value

    def modify(self, r_type, value, origin: str = None):
        if origin is not None:
            self.applied_attributes[origin] = ['mod', r_type, value, self._resistances[r_type]]
        self._resistances[r_type] += max(0, value - 1)

    """
    r_types_values_input = {
        'Piercing': ([1, 'ArmourA_ID', 'mod'], [1.1, 'ArmourB_ID', 'mod'], [1.4, 'ArmourC_ID', 'mod'], [0.75, 'ArmourD_ID', 'mod'], [0.9, 'ArmourE_ID', 'mod']),
        'Blunt': ([1.5, 'ArmourA_ID', 'mod'], [0.9, 'ArmourB_ID', 'mod'], [0.6, 'ArmourC_ID', 'mod'], [1.25, 'ArmourD_ID', 'mod'], [1.1, 'ArmourE_ID', 'mod'])
        }
    set_and_modify(r_types_values_input, True)
    a = [('set', 'armourA'), ('mod', 'armourB'), ('mod', 'armourC')]
    """

    def set_and_modify(self, r_types_values, add_to_list=True):
        for r_type, value_and_origin in r_types_values.items():
            for index, (value, origin, should_set) in enumerate(value_and_origin):
                if not index and should_set:
                    if add_to_list:
                        self.applied_attributes[origin] = ['set', r_type, value, self._resistances[r_type]]
                    self.set(r_type, value)
                else:
                    if add_to_list:
                        self.applied_attributes[origin] = ['mod', r_type, value, self._resistances[r_type]]
                    self.modify(r_type, value)

    def remove_with_origin(self, origin):
        if origin not in self.applied_attributes:
            return
        origin1 = self.applied_attributes[origin]
        if origin1[0] == 'mod':
            self._resistances[origin1[1]] -= origin1[2]
            del self.applied_attributes[origin]
        elif origin1[0] == 'set':
            del self.applied_attributes[origin]
            self.reset_resistances()
            r_types_values = {}
            for origin, [mode, r_type, value, previous] in self.applied_attributes.items():
                if r_type not in r_types_values:
                    r_types_values[r_type] = []
                r_types_values[r_type].append([value, origin, mode])
            self.set_and_modify(r_types_values, False)

    def clone(self):
        a = AttributeSupervisor()
        a._resistances = self._resistances.copy()
        return a


from pprint import pprint
attribute_s = AttributeSupervisor()
attribute_s.set(DamageType.Blunt, 1.5, 'ArmourA')
attribute_s.set(DamageType.Piercing, 1.5, 'ArmourA')
attribute_s.set(DamageType.Air_Elemental, 0.5, 'ArmourA')
attribute_s.set(DamageType.Earth_Elemental, 0.7, 'ArmourC')
pprint(f'{attribute_s.resistances}')
print('--------------------------------')
attribute_s.modify(DamageType.Spectral, 0.5, 'ArmourA')
attribute_s.modify(DamageType.Cutting, 0.1, 'ArmourA')
attribute_s.modify(DamageType.Blunt, 0.1, 'ArmourC')
attribute_s.modify(DamageType.Fire_Elemental, 1.3, 'ArmourC')
pprint(f'{attribute_s.resistances}')
print('--------------------------------')
attribute_s.set_and_modify({DamageType.Piercing: ([1, 'ArmourA', 'mod'], [1.1, 'ArmourB', 'mod'], [1.4, 'ArmourC', 'mod'], [0.75, 'ArmourD', 'mod'], [0.9, 'ArmourE', 'mod']),
                            DamageType.Blunt: ([1.5, 'ArmourA', 'mod'], [0.9, 'ArmourB', 'mod'], [0.6, 'ArmourC', 'mod'], [1.25, 'ArmourD', 'mod'], [1.1, 'ArmourE', 'mod'])})
pprint(f'{attribute_s.resistances}')
print('--------------------------------')
attribute_s.remove_with_origin('ArmourA')
pprint(f'{attribute_s.resistances}')
print('--------------------------------')
