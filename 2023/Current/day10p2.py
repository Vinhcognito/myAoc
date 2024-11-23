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
    def __init__(self, point: Point, type: str, dist: int):
        self.point = point
        self._dist = dist
        self.type = type

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


def get_start_pipe(point: Point, neighbours: list[Point]):
    li = []
    for pt in neighbours:
        if pt - pipe.point == Point(0, -1):  # n
            li.append("1")
        if pt - pipe.point == Point(0, 1):  # s
            li.append("2")
        if pt - pipe.point == Point(1, 0):  # e
            li.append("3")
        if pt - pipe.point == Point(-1, 0):  # w
            li.append("4")
    li.sort()
    typestr = "".join(li)
    match typestr:
        case "12":
            return "|"
        case "13":
            return "L"
        case "14":
            return "J"
        case "23":
            return "F"
        case "24":
            return "7"
        case "34":
            return "-"
        case _:
            logger.exception("S was wrong")


# create main loop starting from S
connected_loop: dict[Point, Pipe] = {}  # {Point:distance_to_start}
todo = [Pipe(start, "S", 0)]
while len(todo) > 0:
    pipe = todo.pop(0)
    connected_loop[Point(pipe.point.x, pipe.point.y)] = Pipe(
        pipe.point, grid.get(pipe.point, "."), pipe.dist
    )
    neighbours = get_valid_neighbours(pipe.point)
    # fill in what S is
    if pipe.type == "S":
        connected_loop[pipe.point].type = get_start_pipe(pipe.point, neighbours)

    if neighbours is not None:
        for pt in neighbours:
            if pt not in connected_loop:
                todo.append(
                    Pipe(pt, grid.get(pt, "."), connected_loop[pipe.point].dist + 1)
                )
            else:
                connected_loop[pipe.point].dist += 1

max_dist_pipe = max(connected_loop.values(), key=lambda pipe: pipe.dist)

print(
    f"Part1 distance to farthest pipe @ {max_dist_pipe.point} is {max_dist_pipe.dist} and is a {max_dist_pipe.type}"
)

# part 2


def check_gap(point: Point) -> list[str]:
    """returns list of dir strs reachable from point if possible else an empty list"""
    # get hori and vertical adjacent tiles
    top = ""
    bot = ""
    left = ""
    right = ""

    if point + Vectors.N in grid:
        if point + Vectors.N in connected_loop:
            top = connected_loop[point - Vectors.N].type
        else:
            top = "."
    if point + Vectors.S in grid:
        if point + Vectors.S in connected_loop:
            bot = connected_loop[point - Vectors.S].type
        else:
            bot = "."
    if point + Vectors.E in grid:
        if point + Vectors.E in connected_loop:
            right = connected_loop[point - Vectors.E].type
        else:
            right = "."
    if point + Vectors.W in grid:
        if point + Vectors.W in connected_loop:
            left = connected_loop[point - Vectors.W].type
        else:
            left = "."

    """
    concat left,right
    concat top,bottom

    ||  |F  |L  J| 7|  

    JF  7F  JL  7L

    - - - J L  
    - F 7 - -

    L L J J
    F 7 F 7
    """
    valid_hori = ["||", "|F", "|L", "J|", "7|", "JF", "7F", "JL", "7L"]
    valid_vert = ["--", "-F", "-7", "J-", "L-", "LF", "L7", "JF", "J7"]

    output = []

    if point in connected_loop:
        pipe = connected_loop[point].type
        # check left and right for gap
        if pipe + right in valid_hori or left + pipe in valid_hori:
            output.extend(["top", "bot"])
        if top + pipe in valid_vert or pipe + bot in valid_vert:
            output.extend(["let", "right"])
        # check for empty space
        if top == ".":
            output.append("top")
        if bot == ".":
            output.append("bot")
        if left == ".":
            output.append("left")
        if right == ".":
            output.append("right")
    return output


def check(point: Point):
    """true for within  false for outside"""
    ray = Point(-1, point.y)
    count = 0
    while True:
        ray = ray + Vectors.E
        # count edges of connected loop travelled past
        if ray == point:
            logger.critical(f"count for {point} is {count}")
            return count % 2 == 1
        if ray in connected_loop:
            tile = connected_loop[ray].type
        else:
            tile = "X"
        match tile:
            case "|" | "J" | "L" | "7" | "F":
                count += 1
                logger.debug(
                    f"ray is @ P({ray.x},{ray.y}) which has a {connected_loop[ray].type}"
                )
                logger.debug(f"count is currently {count}")


def test(x, y):
    logger.debug(f"P({x,y}) is a {grid[Point(x,y)]} and is {check(Point(x,y))}")
    logger.debug(f"{grid[Point(x-1,y-1)]}{grid[Point(x,y-1)]}{grid[Point(x+1,y-1)]}")
    logger.debug(f"{grid[Point(x-1,y)]}{grid[Point(x,y)]}{grid[Point(x+1,y)]}")
    logger.debug(f"{grid[Point(x-1,y+1)]}{grid[Point(x,y+1)]}{grid[Point(x+1,y+1)]}")


"""
unconnected = {}
for point in grid.keys():
    if point not in connected_loop:
        if check(point):
            unconnected[point] = 1
"""


test(14, 3)
