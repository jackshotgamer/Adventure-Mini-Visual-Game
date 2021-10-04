from W_Main_File.Data import Item, Sprites_

rusty_knife = Item.Weapon('Rusty Knife', 'rusty_knifeDefaultWeapon', 6, 10, 8, Item.DamageType.Cutting, False)


null_weapon_1 = Item.Weapon('Nullifier', 'null_weapon_1SpecialWeapon', 0, 200, 10, Item.DamageType.Null | Item.DamageType.Void_Elemental, True)
null_weapon_2 = Item.Weapon('Disannull', 'null_weapon_2SpecialWeapon', 100, 100, 10, Item.DamageType.Null | Item.DamageType.Void_Elemental, True)
