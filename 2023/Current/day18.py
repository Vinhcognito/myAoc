import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from functools import reduce
from pprint import pprint

from helpers import Point, Vectors, get_locations, print_dict_as_array, read_input
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

# sys.setrecursionlimit(2000000)
DAY = 18

locations = get_locations(f"day{DAY}")
# logger.add(f"{locations.log_file}", backtrace=True, diagnose=True)
logger_config(logger)
clear_terminal()

content = read_input(locations.example_file)
rows = content.split("\n")


#  0 means R, 1 means D, 2 means L, and 3 means U.
@dataclass(frozen=True)
class Dig:
    dir: Point
    length: int
    hex: str
    """
    def convert_hex(self):
        dirvals = {
            0: Vectors.E,
            1: Vectors.S,
            2: Vectors.W,
            3: Vectors.N,
        }
        self.length = int(self.hex[:-1], 16)
        self.dir = dirvals[int(self.hex[-1])]
    """


# parse input
digs: list[Dig] = []
for row in rows:
    dirstr, length, hexstr = row.split(" ")
    match dirstr:
        case "U":
            dir = Vectors.N
        case "D":
            dir = Vectors.S
        case "L":
            dir = Vectors.W
        case "R":
            dir = Vectors.E

    digs.append(Dig(dir, int(length), hexstr[2:-1]))


grid: dict[Point, int] = {}

pos = Point(0, 0)
grid[pos] = 1
for dig in digs:
    for i in range(dig.length):
        pos += dig.dir
        grid[pos] = 2

grid_start = Point(min(pt.x for pt in grid), min(pt.y for pt in grid))
grid_end = Point(max(pt.x for pt in grid), max(pt.y for pt in grid))

print(f"grid from {grid_start} to {grid_end}")


def flood(stack: list[Point] = []):
    visited = set()
    while stack:
        point = stack.pop()
        # check if visited
        if point in visited:
            continue
        visited.add(point)
        # fail case
        if point in grid:
            continue
        # check boundary
        elif (
            point.x < grid_start.x
            or point.x > grid_end.x
            or point.y < grid_start.y
            or point.y > grid_end.y
        ):
            continue
        else:
            # if valid, add adjacent to stack
            grid[point] = 0
            stack.append(point + Vectors.N)
            stack.append(point + Vectors.E)
            stack.append(point + Vectors.S)
            stack.append(point + Vectors.W)


stack_start: list[Point] = []
for y in range(grid_start.y, grid_end.y + 1):
    for x in range(grid_start.x, grid_end.x + 1):
        if x == grid_start.x or x == grid_end.x:
            stack_start.append(Point(x, y))
        elif y == grid_start.y or y == grid_end.y:
            stack_start.append(Point(x, y))
        else:
            continue

flood(stack_start)
# count filled tiles
unfilled_area = sum(value == 0 for value in grid.values())
total_area = (grid_end.x + 1 - grid_start.x) * (grid_end.y + 1 - grid_start.y)
print(f"Part 1: filled area={total_area}-{unfilled_area} ={total_area-unfilled_area} ")


# part 2 ----------------------------------------------------------
""" Too slow
grid: dict[Point, int] = {}

pos = Point(0, 0)
grid[pos] = 1
for dig in digs:
    dig.convert_hex()
    for i in range(dig.length):
        pos += dig.dir
        grid[pos] = 2

grid_start = Point(min(pt.x for pt in grid), min(pt.y for pt in grid))
grid_end = Point(max(pt.x for pt in grid), max(pt.y for pt in grid))

print(f"grid from {grid_start} to {grid_end}")


stack_start: list[Point] = []
for y in range(grid_start.y, grid_end.y + 1):
    for x in range(grid_start.x, grid_end.x + 1):
        if x == grid_start.x or x == grid_end.x:
            stack_start.append(Point(x, y))
        elif y == grid_start.y or y == grid_end.y:
            stack_start.append(Point(x, y))
        else:
            continue

flood(stack_start)
unfilled_area = sum(value == 0 for value in grid.values())
total_area = (grid_end.x + 1 - grid_start.x) * (grid_end.y + 1 - grid_start.y)
print(f"Part 2: filled area is {total_area-unfilled_area}")
"""
