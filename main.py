from constants import *
from unicurses import *
from random import choice
from items import Item, Coin
stdscr = initscr()

if __name__ != "__main__":
    exit()

clear()
curs_set(False)
keypad(scr_id=stdscr, yes=True)

PLAYER_DATA = { # attack without anything is 1
    "coins": 0,
    "health": 100,
    "health-max": 100,
    "inventory": {},
    "equipped": []
}
GAMESTATE = [0]
TMP_DATA = [0] # is used for selections
SELECTION_OPTIONS = [-1, 0] # [optioncount || -1 to deactivate, TMP_DATA index to store state]
MESSAGES = []

def calculateAttack() -> int:
    return 1

def calculateDefense() -> int:
    return 1

def print_header():
    width = 9
    addstr(f"---  Coins: {str(PLAYER_DATA['coins']).rjust(width-1)}⛃   Attack: {str(calculateAttack()).rjust(width)}\n")
    health = f"{PLAYER_DATA['health']}/{PLAYER_DATA['health-max']}".rjust(width)
    addstr(f"--- Health: {health}  Defense: {str(calculateDefense()).rjust(width)}\n\n")

def print_option_list(options, index=0):
    global SELECTION_OPTIONS
    for n, option in enumerate(options):
        addstr(f"  ({'+' if TMP_DATA[SELECTION_OPTIONS[1]] == n else ' '}) {option}\n")
    SELECTION_OPTIONS = [len(options), index]

def print_gamestate():

    # HOME
    if GAMESTATE[0] == 0:
        addstr("You are currently at home. Where would you like to go?\n\n")
        options = ["Dungeon", "Smithy", "Exit"]
        print_option_list(options)

    # DUNGEON
    if GAMESTATE[0] == 1:
        # has to be if because GAMESTATE is gradually being filled, therefore they might be executed in series
        if len(GAMESTATE) == 1: # dungeon has not been chosen yet
            addstr("You stand in front of many doors, leading to many different dungeons. Which would you like to enter?\n\n")
            options = ["Dungeon 1", "Dungeon 2", "Dungeon 3", "Return"]
            print_option_list(options)
        if len(GAMESTATE) == 2: # dungeon has just been entered; GAMESTATE = [1, DUNGEON_LEVEL]
            GAMESTATE.append((GAMESTATE[1] + 1) * 5) # add how many enemies have to be fought to clear the dungeon
        if len(GAMESTATE) == 3: # either upon dungeon creation or after defeating an enemy; GAMESTATE = [1, DUNGEON_LEVEL, ENEMIES_UNTIL_BOSS]
            if GAMESTATE[2] > 0:
                GAMESTATE.append(choice(DUNGEON_MONSTERS[GAMESTATE[1]]).copy())
            elif GAMESTATE[2] == 0:
                GAMESTATE.append(DUNGEON_BOSSES[GAMESTATE[1]].copy())
        if len(GAMESTATE) == 4: # now we're fighting; GAMESTATE = [1, DUNGEON_LEVEL, ENEMIES_UNTIL BOSS, {}]; {} = current enemy
            addstr(f"You are in the dungeon {GAMESTATE[1] + 1}. Having encountered the enemy number {(GAMESTATE[1] + 1) * 5 - GAMESTATE[2] + 1}, which is a {GAMESTATE[3].name}, what do you want to do?\n\n")
            options = ["Attack", "Flee"]
            print_option_list(options)

    # SMITHY
    if GAMESTATE[0] == 2:
        if len(GAMESTATE) == 1:
            addstr("You are currently in the smithy. What would you like to do?\n\n")
            options = ["Sell", "Combine", "Return"]
            print_option_list(options)
        elif len(GAMESTATE) == 2:
            if GAMESTATE[1] == 0: # Sell
                if len(PLAYER_DATA["inventory"]) <= 0:
                    addstr("You are currently in the smithy, but you don't have anything to sell.\n\n")
                    options = ["Return"]
                    print_option_list(options)
                else:
                    addstr("You are currently in the smithy. What would you like to sell?\n\n")
                    options = [f"{amount} * {item.type.capitalize().ljust(20, ' ')}:{item.determine_price()}⛃" for item, amount in PLAYER_DATA["inventory"].items()] + ["Return"]
                    print_option_list(options)
            elif GAMESTATE[1] == 1: # Combine
                pass
        # display inventory
        # if len(PLAYER_DATA["inventory"]) > 0:
        #     for item, amount in PLAYER_DATA["inventory"].items():
        #         addstr(f"  {amount} * {item.type.capitalize().ljust(20, ' ')}\n")
        # else:
        #     addstr("  You have no items.")
    
    addstr("\n")
    for message in MESSAGES:
        addstr(f"\n{message}")

def handle_input(ch: int):
    global GAMESTATE, SELECTION_OPTIONS, MESSAGES
    if ch == ESC: # quick exit
        print("Exited gracefully")
        exit()
    if ch == RETURN:
        MESSAGES = []
    if SELECTION_OPTIONS[0] >= 0: # if in selection, just handle selection code
        if ch == UP:
            TMP_DATA[SELECTION_OPTIONS[1]] = (TMP_DATA[SELECTION_OPTIONS[1]] + SELECTION_OPTIONS[0] - 1) % SELECTION_OPTIONS[0]
            return # to not execute the code for HOME, DUNGEON, ...
        elif ch == DOWN:
            TMP_DATA[SELECTION_OPTIONS[1]] = (TMP_DATA[SELECTION_OPTIONS[1]] + SELECTION_OPTIONS[0] + 1) % SELECTION_OPTIONS[0]
            return # to not execute the code for HOME, DUNGEON, ...
        elif ch == RETURN:
            SELECTION_OPTIONS[0] = -2 # indicate that selection has been done
        else:
            return
    
    # this point only gets crossed if something was selected (ch == RETURN)

    # HOME
    if GAMESTATE[0] == 0: 
        if len(GAMESTATE) == 1:
            if TMP_DATA[SELECTION_OPTIONS[1]] == 0: # Dungeon
                GAMESTATE = [1]
            elif TMP_DATA[SELECTION_OPTIONS[1]] == 1: # Smithy
                GAMESTATE = [2]
            elif TMP_DATA[SELECTION_OPTIONS[1]] == 2: # Exit
                print("Exited gracefully"); exit()

    # DUNGEON
    elif GAMESTATE[0] == 1: 
        if len(GAMESTATE) == 1: # only if in choosing dungeons
            if TMP_DATA[SELECTION_OPTIONS[1]] in [0, 1, 2]:
                GAMESTATE = [1, TMP_DATA[SELECTION_OPTIONS[1]]]
            elif TMP_DATA[SELECTION_OPTIONS[1]] == 3:
                GAMESTATE = [0]
        elif len(GAMESTATE) == 4:
            if TMP_DATA[SELECTION_OPTIONS[1]] == 0: # attack
                player_damage = calculateAttack()
                GAMESTATE[3].health = max(GAMESTATE[3].health - player_damage, 0) # player damages enemy
                MESSAGES.append(f"You damaged the {GAMESTATE[3].name} for {player_damage} damage.")

                # enemy still alive
                if GAMESTATE[3].health > 0:
                    PLAYER_DATA["health"] = max(0, PLAYER_DATA["health"] - GAMESTATE[3].attack) # enemy damages player
                    MESSAGES.append(f"{GAMESTATE[3].name} attacked you and dealt {GAMESTATE[3].attack} damage.")
                    if PLAYER_DATA["health"] <= 0: # if player dies
                        GAMESTATE = [0]
                        MESSAGES.append(f"You died and were ejected from the dungeon.")
                
                # enemy dead
                else:
                    MESSAGES.append(f"You have defeated the {GAMESTATE[3].name}!")
                    loot = (choice(DUNGEON_MONSTERS_LOOT[GAMESTATE[1]] if GAMESTATE[2] > 0 else DUNGEON_BOSSES_LOOT[GAMESTATE[1]])).copy()

                    # add loot to inventory
                    if type(loot) is Coin:
                        MESSAGES.append(f"You received {loot.amount} coins!")
                        PLAYER_DATA["coins"] += loot.amount
                    elif type(loot) is Item:
                        MESSAGES.append(f"You picked up a {loot.type}!")
                        PLAYER_DATA["inventory"][loot] = PLAYER_DATA["inventory"][loot] + 1 if loot in PLAYER_DATA["inventory"] else 1 # in case it is not yet in the inventory
                    
                    GAMESTATE[2] -= 1 # advance one enemy
                    GAMESTATE.pop(3) # remove enemy (indicates that a new one should be added in handle_input)
            elif TMP_DATA[SELECTION_OPTIONS[1]] == 1: # flee
                MESSAGES.append("You fled from the dungeon.")
                GAMESTATE = [0]
    
    # SMITHY
    elif GAMESTATE[0] == 2:
        if len(GAMESTATE) == 1: # only if in selection screen: Sell, Combine, Return
            if TMP_DATA[SELECTION_OPTIONS[1]] == 0:
                GAMESTATE = [2, 0] # -> Sell
            if TMP_DATA[SELECTION_OPTIONS[1]] == 1:
                GAMESTATE = [2, 1] # -> Combine TODO implement
            if TMP_DATA[SELECTION_OPTIONS[1]] == 2:
                GAMESTATE = [0] # Return
        elif len(GAMESTATE) == 2: # now in Sell || Combine
            if GAMESTATE[1] == 0: # Sell
                if TMP_DATA[SELECTION_OPTIONS[1]] == len(PLAYER_DATA["inventory"]): # Return was selected
                    GAMESTATE = [2]
                else:
                    selected_item: Item = list(PLAYER_DATA["inventory"].keys())[TMP_DATA[SELECTION_OPTIONS[1]]]
                    # try: # in case it does not exist
                    PLAYER_DATA["inventory"][selected_item] -= 1
                    PLAYER_DATA["coins"] += selected_item.determine_price()
                    MESSAGES.append(f"You sold {selected_item.type} for {selected_item.determine_price()}⛃")
                    if PLAYER_DATA["inventory"][selected_item] <= 0:
                        del PLAYER_DATA["inventory"][selected_item]
            elif GAMESTATE[1] == 1: # Combine
                pass

    if SELECTION_OPTIONS[0] == -2: # revert to no selection
        SELECTION_OPTIONS[0] = -1
        TMP_DATA[SELECTION_OPTIONS[1]] = 0



while True:
    clear()
    print_header()
    print_gamestate()
    handle_input(getch())