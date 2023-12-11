import re
from collections import Counter
from dataclasses import dataclass, field
from functools import reduce
from pprint import pprint

from helpers import Grid, Point, get_locations, read_input
from loguru import logger
from util import (
    clear_terminal,
    extend_list,
    extend_list_2D,
    extend_list_rect,
    logger_config,
    print_array,
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


content = read_input(locations.input_file)
cl = content.split("\n")

grid = {}
for y, line in enumerate(cl):
    for x, c in enumerate(line):
        if c != ".":
            grid[Point(x, y)] = c
            if c == "S":
                start = Point(x, y)


def get_valid_neighbours(point: Point):
    """returns list of Points that are validly connected to point or None"""
    li = []
    match grid[point]:
        case "S":
            li.append(check_N(point))
            li.append(check_S(point))
            li.append(check_E(point))
            li.append(check_W(point))
        case "|":
            li.append(check_N(point))
            li.append(check_S(point))
        case "-":
            li.append(check_E(point))
            li.append(check_W(point))
        case "L":
            li.append(check_N(point))
            li.append(check_E(point))
        case "J":
            li.append(check_N(point))
            li.append(check_W(point))
        case "7":
            li.append(check_S(point))
            li.append(check_W(point))
        case "F":
            li.append(check_S(point))
            li.append(check_E(point))
        case ".":
            return None

    output = list(filter(lambda x: x is not None, li))
    if len(output) == 0:
        return None
    else:
        return output


def check_N(point: Point):
    try:
        check_pipe = grid[Point(point.x, point.y - 1)]
        if check_pipe == "|" or check_pipe == "F" or check_pipe == "7":
            return Point(point.x, point.y - 1)
        else:
            return None
    except KeyError:
        return None


def check_S(point: Point):
    try:
        check_pipe = grid[Point(point.x, point.y + 1)]
        if check_pipe == "|" or check_pipe == "J" or check_pipe == "L":
            return Point(point.x, point.y + 1)
        else:
            return None
    except KeyError:
        return None


def check_E(point: Point):
    try:
        check_pipe = grid[Point(point.x + 1, point.y)]
        if check_pipe == "-" or check_pipe == "J" or check_pipe == "7":
            return Point(point.x + 1, point.y)
        else:
            return None
    except KeyError:
        return None


def check_W(point: Point):
    try:
        check_pipe = grid[Point(point.x - 1, point.y)]
        if check_pipe == "-" or check_pipe == "F" or check_pipe == "L":
            return Point(point.x - 1, point.y)
        else:
            return None
    except KeyError:
        return None


class Pipe:
    def __init__(self, point: Point, dist: int):
        self.point = point
        self._dist = dist

    @property
    def dist(self):
        return self._dist

    @dist.setter
    def dist(self, value):
        if value < self._dist:
            self._dist = value

    def __eq__(self, other):
        return self.point == other.point

    def __str__(self):
        return f"Pipe({self.point.x,self.point.y}), dist:{self.dist}"


# create main loop starting from S
mainloop = {}  # {Point:distance_to_start}
todo = [Pipe(start, 0)]
while len(todo) > 0:
    pipe = todo.pop(0)
    mainloop[Point(pipe.point.x, pipe.point.y)] = Pipe(pipe.point, pipe.dist)
    neighbours = get_valid_neighbours(pipe.point)
    if neighbours is not None:
        for p in neighbours:
            if p not in mainloop:
                todo.append(Pipe(p, mainloop[pipe.point].dist + 1))
            else:
                mainloop[pipe.point].dist += 1

max_dist_pipe = max(mainloop.values(), key=lambda pipe: pipe.dist)

print(
    f"Part1 distance to farthest pipe @ {max_dist_pipe.point} is {max_dist_pipe.dist}"
)
