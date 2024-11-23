import re
from collections import Counter
from dataclasses import dataclass, field
from functools import reduce
from pprint import pprint

from helpers import Grid, Point, Vectors, get_locations, read_input
from loguru import logger
from util import (
    clear_terminal,
    extend_list,
    extend_list_2D,
    extend_list_rect,
    logger_config,
    print_array,
    wait_for_input,
)

DAY = 10

locations = get_locations(f"day{DAY}")
# logger.add(f"{locations.log_file}", backtrace=True, diagnose=True)
logger_config(logger)
clear_terminal()

"""
| NS 
- EW
L NE
J NW
7 SW
F SE
. 
S is the starting position of the animal
"""


content = read_input(locations.example_file)
cl = content.split("\n")


grid = {}


for y, line in enumerate(cl):
    for x, c in enumerate(line):
        grid_width = len(line)
        grid[Point(x, y)] = c
        if c == "S":
            start = Point(x, y)

grid_height = len(cl)

grid2 = []
for x, line in enumerate(cl):
    grid2.append([])
    for y, c in enumerate(line):
        match c:
            case "." | "-" | "S" | "|":
                grid2[x].append(c)
            case "F" | "J":
                grid2[x].append("/")
            case "7" | "L":
                grid2[x].append("\\")

print_array(grid2)
