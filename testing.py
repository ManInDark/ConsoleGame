from constants import *
from unicurses import *
stdscr = initscr()

clear()
curs_set(False)
keypad(scr_id=stdscr, yes=True)

WAITING = 0
SELECTING = 1
GAMESTATE = [WAITING]
CURRENT_OPTION = 0

while True:
    if GAMESTATE[0] == WAITING:
        ch = getch()
        if ch == UP: # 450
            addstr("^")
        elif ch == DOWN: # 456
            addstr("v")
        elif ch == LEFT: # 452
            addstr("<")
        elif ch == RIGHT: # 454
            addstr(">")
            GAMESTATE = SELECTING
        elif ch == ESC: # 10
            break
        else:
            addstr(ch)
    elif GAMESTATE[0] == SELECTING:
        clear()
        options = ["first", "second", "third"]
        addstr("Options:\n")
        for n in range(len(options)):
            addstr(f"  ({'+' if CURRENT_OPTION == n else ' '}) {options[n]}\n")
        ch = getch()
        if ch == UP:
            CURRENT_OPTION = (CURRENT_OPTION + len(options) - 1) % len(options)
        elif ch == DOWN:
            CURRENT_OPTION = (CURRENT_OPTION + len(options) + 1) % len(options)
        elif ch == RETURN:
            GAMESTATE = WAITING
            print(CURRENT_OPTION+1, "was selected")
    elif GAMESTATE == -1:
        addstr(int(getch()))