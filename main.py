from constants import *
from unicurses import *
stdscr = initscr()

if __name__ != "__main__":
    exit()

clear()
curs_set(False)
keypad(scr_id=stdscr, yes=True)

PLAYER_DATA = {
    "coins": 0,
    "health": 100,
    "health-max": 100,
    "inventory": [],
    "equipped": []
}
GAMESTATE = [0]
TMP_DATA = [0] # [0] is used for selections
SELECTION_OPTIONS = [-1, 0] # [optioncount || -1 to deactivate, TMP_DATA index to store state]

def print_header():
    addstr(f"--- Coins: {PLAYER_DATA['coins']}\n")
    addstr(f"--- Health: {PLAYER_DATA['health']}/{PLAYER_DATA['health-max']}\n")
    addstr(f"---\n\n")

def print_option_list (options):
    global SELECTION_OPTIONS
    for n, option in enumerate(options):
        addstr(f"  ({'+' if TMP_DATA[SELECTION_OPTIONS[1]] == n else ' '}) {option}\n")
    SELECTION_OPTIONS = [len(options), 0]

def print_gamestate():

    # HOME
    if GAMESTATE[0] == 0:
        addstr("You are currently at home. Where would you like to go?\n\n")
        options = ["Dungeon", "Smithy", "Exit"]
        print_option_list(options)

    # DUNGEON
    if GAMESTATE[0] == 1:
        if len(GAMESTATE) == 1: # dungeon has not been chosen yet
            addstr("You stand in front of many doors, leading to many different dungeons. Which would you like to enter?\n\n")
            options = ["Dungeon 1", "Dungeon 2", "Dungeon 3", "Return"]
            print_option_list(options)
        else: # fighting
            pass

    # SMITHY
    if GAMESTATE[0] == 2:
        addstr("You are currently in the smithy. What would you like to do?\n\n")
        pass

def handle_input(ch: int):
    global GAMESTATE, SELECTION_OPTIONS
    if ch == ESC: # quick exit
        print("Exited gracefully")
        exit()
    elif SELECTION_OPTIONS[0] >= 0: # if in selection, just handle selection code
        if ch == UP:
            TMP_DATA[SELECTION_OPTIONS[1]] = (TMP_DATA[SELECTION_OPTIONS[1]] + SELECTION_OPTIONS[0] - 1) % SELECTION_OPTIONS[0]
            return # to not execute the code for HOME, DUNGEON, ...
        elif ch == DOWN:
            TMP_DATA[SELECTION_OPTIONS[1]] = (TMP_DATA[SELECTION_OPTIONS[1]] + SELECTION_OPTIONS[0] + 1) % SELECTION_OPTIONS[0]
            return # to not execute the code for HOME, DUNGEON, ...
        elif ch == RETURN:
            SELECTION_OPTIONS[0] = -2 # indicate that selection has been done
    
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

    if SELECTION_OPTIONS[0] == -2: # revert to no selection
        SELECTION_OPTIONS[0] = -1
        TMP_DATA[SELECTION_OPTIONS[1]] = 0



while True:
    clear()
    print_header()
    print_gamestate()
    handle_input(getch())