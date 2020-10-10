# -*- coding: UTF-8 -*-

import curses
from models import *
from time import sleep
import random
import os

esc_keylist = {'esc', '^[', '^C', '\x03', '\x1b'} 
right_keylist = {'KEY_RIGHT', 'KEY_B3'}
left_keylist = {'KEY_LEFT', 'KEY_B1'}
up_keylist = {'KEY_UP', 'KEY_A2'}
down_keylist = {'KEY_DOWN', 'KEY_C2'}
rainbow_colors = [1, 2, 3, 5, 6]

def win_screen(stdscr):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    stdscr.border('|', '|', '-', '-', '+', '+', '+', '+')
    win_str = "VICTORY!"
    for count in range(0, 3):
        for i in range(0, len(win_str)):
            stdscr.addstr(
                    (int)((height - 1)/2) - 1, 
                    (int)((width - len(win_str))/2) + i, 
                    win_str[i], 
                    curses.color_pair(rainbow_colors[(count + i) % len(rainbow_colors)]))
            stdscr.refresh()
            sleep(.05)
    for i in range(0, len(win_str)):
        stdscr.addstr(
                (int)((height - 1)/2) - 1, 
                (int)((width - len(win_str))/2) + i, 
                win_str[i], 
                curses.color_pair(6))
        stdscr.refresh()
        sleep(.05)
    instr_str = "<ESC> to exit"
    instr2_str ="Any key to play again"
    stdscr.addstr(
        (int)((height - 1)/2) + 1,
        (int)((width - len(instr_str))/2),
        instr_str,
        curses.color_pair(10))
    stdscr.addstr(
        (int)((height - 1)/2) + 2,
        (int)((width - len(instr2_str))/2),
        instr2_str,
        curses.color_pair(10))
    stdscr.refresh()
    key = ""
    while key == "":
        try:
            key = stdscr.getkey()
        except: 
            key = ""
    if key in esc_keylist:
        return False
    else:
        return True

def play_game(stdscr):
    # Clear screen and draw border
    stdscr.clear()
    height,width = stdscr.getmaxyx()

    stdscr.border('|', '|', '-', '-', '+', '+', '+', '+')
    maze = maze_grid(width-4, height-2)
    maze.print_maze(stdscr, curses)
    key = ""

    path = []
    player_x, player_y = maze.x_offset + 1, maze.y_offset + 1
    path.append((player_x, player_y))
    stdscr.addstr(player_y, player_x, '☻' , curses.color_pair(PLAYER_PAIR))

    stdscr.addstr(len(maze.grid[0]) - 1, len(maze.grid), "@", curses.color_pair(9))
    while True:
        try:
            key = stdscr.getkey()
        except:
            key = ""
        moved = False
        prev_x, prev_y = player_x, player_y
        future_x, future_y = player_x, player_y
        if key in left_keylist: #left
            future_x -= 1
            moved = True
        if key in right_keylist: #right
            future_x += 1
            moved = True
        if key in up_keylist: #up
            future_y -= 1
            moved = True
        if key in down_keylist: #down
            future_y += 1
            moved = True
        if moved and future_x == len(maze.grid) and future_y == len(maze.grid[0]) - 1:
            for coord in path:
                px, py = coord
                stdscr.addstr(py, px, ' ' , curses.color_pair(0))
                stdscr.refresh()
                sleep(.01)
            return win_screen(stdscr)
        if moved and maze.check_if_open(future_x - maze.x_offset, future_y - maze.y_offset):
            player_x, player_y  = future_x, future_y     
            path.append((player_x, player_y))
            stdscr.addstr(prev_y, prev_x, '█' , curses.color_pair(PATH_PAIR))
            stdscr.addstr(player_y, player_x, '☻' , curses.color_pair(PLAYER_PAIR))
        stdscr.refresh()
        if key in esc_keylist:
            return False

os.environ.setdefault('ESCDELAY', '25')

stdscr = curses.initscr()
curses.start_color()
curses.halfdelay(1)           # How many tenths of a second are waited, from 1 to 255
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.curs_set(False)


for i in range(1, 11):
    curses.init_pair(i, i, curses.COLOR_BLACK)

curses.init_pair(PLAYER_PAIR, PLAYER_COLOR, PATH_COLOR)
curses.init_pair(PATH_PAIR, PATH_COLOR, curses.COLOR_BLACK)

play_on = True
while play_on:
    play_on = play_game(stdscr)

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.curs_set(True)
curses.endwin()
