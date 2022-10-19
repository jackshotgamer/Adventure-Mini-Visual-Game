from W_Main_File.Data import HpEntity, Sprites_
from W_Main_File.Utilities import Vector


class EnemyData(HpEntity.HpEntity):
    def __init__(self, name, max_hp, hp, gold, xp, lvl, floor):
        super().__init__(name, Vector.Vector(0, 0), max_hp, hp, gold, xp, lvl, floor)

    def choose_action(self, target, **options):
        from W_Main_File.Data import Item
        data = {
            'attack_name': 'Swirling Sword of Doom',
            'attack_damage': 5,
            'attack_type': Item.DamageType.Cutting & Item.DamageType.Air_Elemental
        }
        return data


enemy_possibilities = {
    'Death Knight': lambda: EnemyData('Death Knight', 100, 100, 20, 10, 1, 1),
    'Devouring Horror': lambda: EnemyData('Devouring Horror', 100, 100, 20, 10, 1, 1),
    'Golden Serpent': lambda: EnemyData('Golden Serpent', 100, 100, 20, 10, 1, 1),
    'Offspring of Shrub Niggurath': lambda: EnemyData('Offspring of Shrub Niggurath', 100, 100, 20, 10, 1, 1),
    'Purgatory Dragon Skeleton': lambda: EnemyData('Purgatory Dragon Skeleton', 100, 100, 20, 10, 1, 1),
    'Troglodyte': lambda: EnemyData('Troglodyte', 200, 200, 50, 7, 1, 1),
    'Troglodyte Hellebardier': lambda: EnemyData('Troglodyte Hellebardier', 150, 150, 25, 5, 1, 1),
}
