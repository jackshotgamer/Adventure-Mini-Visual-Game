from W_Main_File.Data import Item, Sprites_

item_dict = {
    'rusty_knife': lambda: Item.Weapon('Rusty Knife', 'rusty_knifeDefaultWeapon', 6, 10, 8, 1, Item.DamageType.Cutting, False),
    'nullifier': lambda: Item.Weapon('Nullifier', 'null_weapon_1SpecialWeapon', 0, 200, 10, 10, Item.DamageType.Null | Item.DamageType.Void_Elemental, True),
    'disannull': lambda: Item.Weapon('Disannull', 'null_weapon_2SpecialWeapon', 100, 100, 10, 10, Item.DamageType.Null | Item.DamageType.Void_Elemental, True),
}


def __getattr__(name):
    return item_dict[name]()
