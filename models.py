# -*- coding: UTF-8 -*-

from typing import List
import random

PLAYER_PAIR = 15
PATH_PAIR = 13
WALL_COLOR = 8
PATH_COLOR = 5
OPEN_COLOR = 5
PLAYER_COLOR = 10
WALL_CHAR = '█'
OPEN_CHAR = ' '
PATH_CHAR = '.'

class cell:
    def __init__(self, x, y, data: str, color: int) -> None:
        self.x = x
        self.y = y
        self.data = data
        self.color = color

class maze_grid:
    def __init__(self, width: int, height: int) -> None:
        """ Construct grid and carve maze """
        # make sure there are an odd number of rows and cols
        if width % 2 == 0:
            width -= 1
        if height % 2 == 0:
            height -= 1
        self.width = width
        self.height = height
        self.x_offset = 0
        self.y_offset = 0
        self.grid : List[List[cell]] = []
        for i in range(0, width):
            col = []
            for j in range(0, height):
                col.append(cell(i, j, WALL_CHAR, WALL_COLOR))
            self.grid.append(col)
        self.carve_maze()

    def conv_grid_to_game_coords(self, game_x, game_y):
        return (game_x - 1)/2, (game_y - 1)/2

    def conv_game_to_grid_coords(self, grid_x, grid_y):
        return grid_x * 2 + 1, grid_y * 2 + 1

    def carve_maze(self) -> None:
        # carves out maze using aldous-broder algorithm
        # cell count
        game_x = 0
        game_y = 0
        grid_x, grid_y = self.conv_game_to_grid_coords(game_x, game_y)
        prev_grid_x, prev_grid_y = grid_x, grid_y
        prev_game_x, prev_game_y = game_x, game_y
        self.grid[grid_x][grid_y].data = OPEN_CHAR
        self.grid[grid_x][grid_y].color = OPEN_COLOR

        max_right, max_bottom = self.conv_grid_to_game_coords(self.width, self.height)
        cell_count =  max_right * max_bottom
        max_bottom -= 1
        max_right -= 1
        filled_cells = 1
        while (filled_cells < cell_count):
            moved = False
            while not moved:
                prev_grid_x, prev_grid_y = grid_x, grid_y
                prev_game_x, prev_game_y = game_x, game_y
                direction = random.choice(['L','R','U','D'])
                if direction == 'L' and game_x > 0:
                    game_x -= 1   
                    moved = True
                elif direction == 'R' and game_x < max_right:
                    game_x += 1   
                    moved = True
                elif direction == 'U' and game_y > 0:  
                    game_y -= 1   
                    moved = True
                elif direction == 'D' and game_y < max_bottom:
                    game_y += 1   
                    moved = True
            grid_x, grid_y = self.conv_game_to_grid_coords(game_x, game_y)
            if self.grid[grid_x][grid_y].data == WALL_CHAR:
                self.grid[grid_x][grid_y].data = OPEN_CHAR
                self.grid[grid_x][grid_y].color = OPEN_COLOR
                filled_cells += 1
                border_x, border_y = (int)((prev_grid_x + grid_x)/2) , (int)((prev_grid_y + grid_y)/2)
                if self.grid[border_x][border_y].data == WALL_CHAR:
                    self.grid[border_x][border_y].data = OPEN_CHAR
                    self.grid[border_x][border_y].color = OPEN_COLOR


    def check_if_open(self, grid_x, grid_y) -> bool:
        if grid_x < 0 and grid_x > self.width:
            return False
        if grid_y < 0 and grid_y > self.height:
            return False
        return self.grid[grid_x][grid_y].data == OPEN_CHAR

    def print_maze(self, stdscr, curses) -> None:
        height,width = stdscr.getmaxyx()
        self.x_offset = (int)((width - self.width) / 2)
        self.y_offset = (int)((height - self.height) / 2)
        for x in range(0, self.width):
            for y in range(0, self.height):
                current_cell = self.grid[x][y]
                stdscr.addstr(y + self.y_offset, x + self.x_offset, current_cell.data , curses.color_pair(current_cell.color))
        stdscr.refresh()
