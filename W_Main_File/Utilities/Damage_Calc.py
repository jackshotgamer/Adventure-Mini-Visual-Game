import random

from W_Main_File.Data import HpEntity


def calculate_damage(damage, elements, target: HpEntity.HpEntity):
    from W_Main_File.Data.Item import DamageType
    if elements & (DamageType.Any_Elemental & ~DamageType.Void_Elemental):
        elemental_damage = damage * 0.2
    elif elements & DamageType.Void_Elemental:
        elemental_damage = damage * 0.4
    else:
        elemental_damage = 0
    resistances = target.resistances
    total_damage = (damage * resistances[elements & DamageType.Any_Basic]) + (elemental_damage * resistances[elements & DamageType.Any_Elemental])
    return int(total_damage)
