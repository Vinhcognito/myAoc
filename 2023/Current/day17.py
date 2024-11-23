import re
from collections import Counter
from dataclasses import dataclass, field
from functools import reduce
from pprint import pprint

from helpers import Point, Vectors, get_locations, read_input
from loguru import logger
from util import (
    clear_terminal,
    extend_list,
    extend_list_2D,
    extend_list_rect,
    logger_config,
    print_array,
    sign,
)

DAY = 17

locations = get_locations(f"day{DAY}")
# logger.add(f"{locations.log_file}", backtrace=True, diagnose=True)
logger_config(logger)
clear_terminal()

content = read_input(locations.example_file)
rows = content.split("\n")

grid = []
for y, row in enumerate(rows):
    grid.append([])
    for x, num in enumerate(row):
        grid[y].append(int(num))

grid_height = len(rows)
grid_width = len(rows[0])

min_heat = None


def walk(start: Point, vector: Point, heat: int):
    step = Point(sign(vector.x), sign(vector.y))
    dest = start + vector

    # calc added heat
    while start != dest:
        start += step
        heat += grid[start.x][start.y]

    if dest == Point(grid_width - 1, grid_height - 1):
        # BASE CASE
        print(f"Reached the End, heat of :{heat}")
        return
    else:
        # RECURSIVE CASE
        for i in range(1,4):
            for d in [left,right]
        walk()

        # After recursive call
        # print(number, "returning")
        return


"""
for a maze:
    
    What is the base case? 
        Reaching a dead end or the exit of the maze.
    What argument is passed to the recursive function call? 
        The x, y coordinates, along with the maze data and list of already visited x, y coordinates.
    How does this argument become closer to the base case? 
       the x, y coordinates keep moving to neighboring coordinates until they eventually reach dead ends or the final exit.

"""
