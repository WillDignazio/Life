import curses
import time
import copy

# Global State
BOARD_EMPTY_CHAR = '.'
BOARD_CELL_CHAR = '#'
BOARD_WIDTH = 120
BOARD_HEIGHT = 60

def init_board():
    state = []
    for hdx in range(BOARD_HEIGHT):
        row = []
        for wdx in range(BOARD_WIDTH):
            row.append(BOARD_EMPTY_CHAR)
        state.append(row)
    return state

def user_setup(stdscr, board, state):
    curses.curs_set(1)
    board.move(1, 1)

    board.refresh()

    cursory = 1
    cursorx = 1
    
    while True:
        ch = stdscr.getch()
        if ch is ord('\r') or ch is ord('\n'):
            break

        if ch == curses.KEY_RIGHT and cursorx < BOARD_WIDTH:
            cursorx += 1
        elif ch == curses.KEY_LEFT and cursorx > 1:
            cursorx -= 1
        elif ch == curses.KEY_UP and cursory > 1:
            cursory -= 1
        elif ch == curses.KEY_DOWN and cursory < BOARD_HEIGHT:
            cursory += 1
        elif ch == ord(' '):
            if state[cursory][cursorx] == BOARD_EMPTY_CHAR:
                state[cursory][cursorx] = BOARD_CELL_CHAR
            else:
                state[cursory][cursorx] = BOARD_EMPTY_CHAR

        stdscr.addstr(0, 0, "Cursor: ({}, {})".format(cursory, cursorx))
        stdscr.refresh()

        draw_board(board, state)

        board.move(cursory, cursorx)
        board.refresh()

    curses.curs_set(0)
    board.refresh()

def draw_board(win, state):
    for y in range(1, BOARD_HEIGHT):
        for x in range(1, BOARD_WIDTH):
            try:
                cell = state[y][x]
                if cell == BOARD_EMPTY_CHAR:
                    win.addch(y, x, BOARD_EMPTY_CHAR)
                else:
                    win.addch(y,x, state[y][x], curses.color_pair(1))
            except curses.error:
                pass
    win.box()
    win.refresh()

def getCell(state, y, x):
    if y >= BOARD_HEIGHT or y < 1:
        return BOARD_EMPTY_CHAR
    elif x >= BOARD_WIDTH or x < 1:
        return BOARD_EMPTY_CHAR
    else:
        return state[y][x]
    
def update_board(state):
    newState = copy.deepcopy(state)

    for hdx in range(BOARD_HEIGHT):
        for wdx in range(BOARD_WIDTH):
            cells = [
                getCell(state, hdx-1, wdx-1),
                getCell(state, hdx-1, wdx),
                getCell(state, hdx-1, wdx+1),
                getCell(state, hdx, wdx-1),
                getCell(state, hdx, wdx+1),
                getCell(state, hdx+1, wdx-1),
                getCell(state, hdx+1, wdx),
                getCell(state, hdx+1, wdx+1)
            ]
            neighbours = sum(cell == BOARD_CELL_CHAR for cell in cells)

            if neighbours == 3 and state[hdx][wdx] == BOARD_EMPTY_CHAR:
                newState[hdx][wdx] = BOARD_CELL_CHAR
            elif neighbours < 2:
                newState[hdx][wdx] = BOARD_EMPTY_CHAR
            elif neighbours > 3:
                newState[hdx][wdx] = BOARD_EMPTY_CHAR
    
    return newState
    
def run(stdscr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    
    state = init_board()

    theight, twidth = stdscr.getmaxyx()
    centery = (theight / 2) - (BOARD_HEIGHT / 2)
    centerx = (twidth / 2) - (BOARD_WIDTH / 2)

    stdscr.addstr(theight-2, 0, "Screen Size: ({}, {})".format(theight, twidth))
    stdscr.addstr(theight-1, 0, "Center: ({}, {})". format(centery, centerx))

    boardWindow = curses.newwin(BOARD_HEIGHT+1, BOARD_WIDTH+1, centery, centerx)
    
    stdscr.refresh()
    draw_board(boardWindow, state)

    user_setup(stdscr, boardWindow, state)

    generation = 0
    while True:
        stdscr.addstr(0, 0, "Generation: {} ".format(generation))
        stdscr.refresh()
        
        # ch = stdscr.getch()
        # if ch is ord('\r') or ch is ord('\n'):
        #     break

        time.sleep(0.01)
        
        state = update_board(state)
        generation += 1
    
        draw_board(boardWindow, state)
        
    stdscr.getch()
            
if __name__ == "__main__":
    curses.wrapper(run)
    
