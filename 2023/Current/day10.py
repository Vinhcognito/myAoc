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


# create main loop starting from S
connected_loop: dict[Point, Pipe] = {}  # {Point:distance_to_start}
todo = [Pipe(start, "S", 0)]
while len(todo) > 0:
    pipe = todo.pop(0)
    connected_loop[Point(pipe.point.x, pipe.point.y)] = Pipe(
        pipe.point, grid.get(pipe.point, "."), pipe.dist
    )
    neighbours = get_valid_neighbours(pipe.point)
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


# =============================part 2 =============================
# unconnected pipes are gaps


def get_reachable(point: Point, dir: Point = None) -> list[Point]:
    """Part2 :returns list of Points that is reachable in the direction specified or empty list"""
    li = []
    match dir:
        case None:
            li.extend(check_T(point))
            li.extend(check_B(point))
            li.extend(check_L(point))
            li.extend(check_R(point))
        case Vectors.N:
            li.extend(check_T(point))
        case Vectors.S:
            li.extend(check_B(point))
        case Vectors.W:
            li.extend(check_L(point))
        case Vectors.E:
            li.extend(check_R(point))
        case _:
            return []
    output = list(set(li))
    if len(output) > 0:
        return output
    else:
        return []


def check_T(point: Point):
    checked_point = point + Vectors.N
    try:
        if checked_point in outside:
            return []
        elif checked_point in connected_loop:
            li = list(
                filter(lambda x: x != point + Vectors.S, check_gap(checked_point))
            )
            return li
        else:
            outside[checked_point] = 1
            return [checked_point]
    except KeyError:
        return []


def check_B(point: Point):
    checked_point = point + Vectors.S
    try:
        if checked_point in outside:
            return []
        elif checked_point in connected_loop:
            li = list(
                filter(lambda x: x != point + Vectors.N, check_gap(checked_point))
            )
            return li
        else:
            outside[checked_point] = 1
            return [checked_point]
    except KeyError:
        return []


def check_R(point: Point):
    checked_point = point + Vectors.E
    try:
        if checked_point in outside:
            return []
        elif checked_point in connected_loop:
            li = list(
                filter(lambda x: x != point + Vectors.W, check_gap(checked_point))
            )
            return li
        else:
            outside[checked_point] = 1
            return [checked_point]
    except KeyError:
        return []


def check_L(point: Point):
    checked_point = point + Vectors.W
    try:
        if checked_point in outside:
            return []
        elif checked_point in connected_loop:
            li = list(
                filter(lambda x: x != point + Vectors.E, check_gap(checked_point))
            )
            return li
        else:
            outside[checked_point] = 1
            return [checked_point]
    except KeyError:
        return []


def check_gap(point: Point) -> list[str]:
    """returns list of points reachable from point if possible else an empty list"""
    # get hori and vertical adjacent tiles
    top = ""
    bot = ""
    left = ""
    right = ""
    if point + Vectors.N in grid:
        if (point + Vectors.N) in connected_loop:
            top = connected_loop[point + Vectors.N].type
        else:
            top = "."
    if point + Vectors.S in grid:
        if point + Vectors.S in connected_loop:
            bot = connected_loop[point + Vectors.S].type
        else:
            bot = "."
    if point + Vectors.E in grid:
        if point + Vectors.E in connected_loop:
            right = connected_loop[point + Vectors.E].type
        else:
            right = "."
    if point + Vectors.W in grid:
        if point + Vectors.W in connected_loop:
            left = connected_loop[point + Vectors.W].type
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
            output.extend([point + Vectors.N, point + Vectors.S])
        if top + pipe in valid_vert or pipe + bot in valid_vert:
            output.extend([point + Vectors.W, point + Vectors.E])
        # check for empty space
        if top == ".":
            output.append(point + Vectors.N)
        if bot == ".":
            output.append(point + Vectors.S)
        if left == ".":
            output.append(point + Vectors.W)
        if right == ".":
            output.append(point + Vectors.E)
    return output


outside: dict[Point, int] = {}  # Point : 1 or 0 = not countable area
boundary: list[tuple[Point, Point]] = []
todo: list[tuple[Point, Point]] = []  # (Point, DirectionVector)

# start from perimeter
for x in range(grid_width + 1):
    for y in range(grid_height + 1):
        if x == 0:
            boundary.append((Point(x, y), Vectors.E))
        elif x == grid_width:
            boundary.append((Point(x, y), Vectors.W))
        elif y == 0:
            boundary.append((Point(x, y), Vectors.S))
        elif y == grid_height:
            boundary.append((Point(x, y), Vectors.N))
        else:
            continue


for b in boundary:
    point = b[0]
    dir = b[1]
    # check if part of main loop
    if point in connected_loop:
        if check_gap(point):
            outside[point] = 0
            todo.append((point, dir))
    else:
        outside[point] = 1
        todo.append((point, dir))

# todo: list[tuple[Point, str]] = [(Point(0, 0), "r")]
# from boundary search for reachable tiles
checked = {}
while len(todo) > 0:
    point, dir = todo.pop(0)
    neighbours = get_reachable(point, dir)
    logger.debug(f"neighbours:{neighbours}")
    logger.critical(todo)
    if len(neighbours) > 0:
        for pt in neighbours:
            logger.debug(f"pt:{pt}")
            checked[pt] = True
            if pt in outside:
                pass
            elif pt in connected_loop:
                gap_pts = check_gap(pt)
                for gap_pt in gap_pts:
                    logger.debug(f"gap_pts:{gap_pts}")
                    if gap_pt not in checked:
                        todo.append((pt, None))
                        checked[gap_pt] = True
            else:
                if pt not in checked:
                    todo.append((pt, dir))
        # wait_for_input()

area = 0
for point in grid.keys():
    if point not in outside and point not in connected_loop:
        area += 1


def test(x, y):
    logger.debug(f"P({x,y}) is a {grid[Point(x,y)]} ")
    if Point(x, y) in outside:
        logger.warning("is outside")
        logger.info(outside[Point(x, y)])
    elif Point(x, y) in connected_loop:
        logger.warning("is part of main loop")
        logger.info(connected_loop[Point(x, y)])
    else:
        logger.warning("is not outside or part of main loop")
    try:
        logger.debug(
            f"{grid[Point(x-1,y-1)]}{grid[Point(x,y-1)]}{grid[Point(x+1,y-1)]}"
        )
    except KeyError:
        logger.debug("===")
    try:
        logger.debug(f"{grid[Point(x-1,y)]}{grid[Point(x,y)]}{grid[Point(x+1,y)]}")
    except KeyError:
        logger.debug("===")
    try:
        logger.debug(
            f"{grid[Point(x-1,y+1)]}{grid[Point(x,y+1)]}{grid[Point(x+1,y+1)]}"
        )
    except KeyError:
        logger.debug("===")


# pprint(outside)

test(2, 6)
