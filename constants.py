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
    ],
    [
        Entity("Ork", 50, 8, 0),
        Entity("Goblin General", 45, 6, 0)
    ],
    [
        Entity("Grand Ork", 100, 12, 0),
        Entity("Goblin King", 90, 10, 0)
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
    ],
    [
        Item("sword", 5, 1),
        Item("chestplate", 5, 1),
        Item("apple", 0, 1),
        Coin(30),
        Coin(35),
        Coin(40)
    ],
    [
        Item("sword", 10, 1),
        Item("chestplate", 10, 1),
        Item("apple", 0, 1),
        Coin(50),
        Coin(55),
        Coin(60)
    ]
]
DUNGEON_BOSSES = [
    Entity("Boss Goblin", 30, 8, 0),
    Entity("Boss Ork", 80, 12, 0),
    Entity("Boss Goblin King", 150, 15, 0)
]
DUNGEON_BOSSES_LOOT = [
    [
        Item("sword", 0, 2),
        Item("chestplate", 0, 2),
        Coin(40)
    ],
    [
        Item("sword", 5, 2),
        Item("chestplate", 5, 2),
        Coin(60)
    ],
    [
        Item("sword", 15, 2),
        Item("chestplate", 15, 2),
        Coin(80)
    ]
]

EMPTY_INVENTORY = {"sword": None, "chestplate": None}