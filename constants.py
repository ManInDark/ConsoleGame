from items import Item, Coin
from monsters import Entity

RETURN = 10
ESC    = 27
UP     = 450
LEFT   = 452
RIGHT  = 454
DOWN   = 456

DUNGEON_MONSTERS = [
    [
        Entity("Slime", 15, 1, 0),
        Entity("Goblin", 10, 4, 0)
    ]
]
DUNGEON_MONSTERS_LOOT = [
    [
        Item("sword", 0, 1),
        Item("chestplate", 0, 1),
        Item("apple", 0, 2),
        Coin(19),
        Coin(20),
        Coin(21)
    ]
]
DUNGEON_BOSSES = [
    Entity("Boss Goblin", 30, 8, 0)
]
DUNGEON_BOSSES_LOOT = [
    [
        Item("sword", 0, 2),
        Item("chestplate", 0, 2),
        Coin(6)
    ]
]

EMPTY_INVENTORY = {"sword": None, "chestplate": None}