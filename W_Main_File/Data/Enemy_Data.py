from W_Main_File.Data import HpEntity, Sprites_
from W_Main_File.Utilities import Vector


class EnemyData(HpEntity.HpEntity):
    def __init__(self, name, max_hp, hp, gold, xp, lvl, floor, sprite):
        super().__init__(name, Vector.Vector(0, 0), max_hp, hp, gold, xp, lvl, floor)
        self.sprite = sprite

    def choose_action(self, target, **options):
        from W_Main_File.Data import Item
        data = {
            'attack_name': 'Swirling Sword of Doom',
            'attack_damage': 5,
            'attack_type': Item.DamageType.Cutting & Item.DamageType.Air_Elemental
        }
        return data


enemy_possibilities = {
    'Witch': lambda: EnemyData('Witch', 100, 100, 20, 10, 1, 1, Sprites_.swamp_monster),
    'Dragon': lambda: EnemyData('Dragon', 200, 200, 50, 7, 1, 1, Sprites_.swamp_monster),
    'Ogre': lambda: EnemyData('Ogre', 150, 150, 25, 5, 1, 1, Sprites_.swamp_monster),
}
