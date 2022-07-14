# Adventure Mini Game (Name Pending)

This project is a tile based 2d exploration game.

You move across a tiled landscape, and any direction, and the view of the 
camera is in a birds eye view.

When moving across the landscape, each tile you move on, depending on the tile, can be a loot tile, 
an enemy tile, a trap tile, portal tile, the home tile (exclusive to 0,0), or nothing at all.

The tiles are generated automatically using the seed (based on the username), and can be
generated infinitely.

There are multiple different visual tiles to choose from, plains, forest, mountain, village, and
portal tile. plains can have a trapped variant, as well as forest, but forest can also be a
loot or enemy tile, mountain tile can be only a loot tile, and village tile can't be
any of them (reference Excuses_Folder.md for future plans).

There is a login page on startup, where you enter a username, and it logs you in using that
usernames details (level, xp, gold, position, etc) if it exists, if not, it creates a default
character. The character data is stored in the PLAYERDATA file, making a folder named using the
username, and having a player file, and an inv file, containing the player data, and the inventory
contents respectively.
