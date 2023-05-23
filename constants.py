RETURN = 10
ESC    = 27
UP     = 450
LEFT   = 452
RIGHT  = 454
DOWN   = 456

DUNGEON_MONSTERS = [
    [
        {"name": "Slime", "health": 15, "health-max": 15, "attack": 1},
        {"name": "Goblin", "health": 10, "health-max": 10, "attack": 4}
    ]
]
DUNGEON_MONSTERS_LOOT = [
    [
        {"type": "sword", "level": 1},
        {"type": "chestplate", "level": 1},
        {"type": "coins", "amount": 2},
        {"type": "coins", "amount": 3},
        {"type": "coins", "amount": 4}
    ]
]
DUNGEON_BOSSES = [
    {"name": "Boss Goblin", "health": 30, "health-max": 30, "attack": 8}
]
DUNGEON_BOSSES_LOOT = [
    [
        {"type": "sword", "level": 1},
        {"type": "chestplate", "level": 1},
        {"type": "coins", "amount": 6}
    ]
]