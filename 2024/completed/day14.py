from __future__ import annotations

import enum
import math
import re
from collections import Counter, defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from functools import reduce
from itertools import combinations
from pprint import pprint
from typing import Any, ItemsView, Type

from shared.decorators import timer
from shared.helpers import Point, Vectors, get_locations, read_input
from shared.util import (
    extend_list,
    extend_list_2D,
    extend_list_rect,
    ints,
    log,
    logger_config,
    logger_enable,
    logger_init,
    print_array,
    strs,
    wait_for_input,
)

DAY = 14

logger_init()
logger_enable(log, f"day{DAY}")

locations = get_locations(f"day{DAY}")

N = Point(0, -1)
E = Point(1, 0)
S = Point(0, 1)
W = Point(-1, 0)
dirs = [N, E, S, W]

ROWS = 103
COLS = 101


def get_neighbours(point: Point) -> list[Point]:
    return [point + vec for vec in dirs]


class Grid:
    emptyrow = ["."] * COLS
    emptygrid = []
    for _ in range(ROWS):
        emptygrid.append(deepcopy(emptyrow))

    def __init__(self, input: list[str]):
        self.g: dict[Point:int] = Counter()
        self.cols = COLS
        self.rows = ROWS
        self.robots = []

        for line in input:
            px, py, vx, vy = ints(line)[0]
            self.robots.append(Robot(Point(px, py), Point(vx, vy)))

        for row in self.emptygrid:
            print("".join(row))

        print("cat")

    def print_grid(self):
        s_grid = deepcopy(self.emptygrid)
        for robot in self.robots:
            s_grid[robot.pos.y][robot.pos.x] = "#"

        for row in s_grid:
            print("".join(row))

        # wait_for_input()

    def check_grid(self):
        d = Counter()

        for robot in self.robots:
            d[robot.pos] += 1

        return all(count < 2 for count in d.values())

    def part_one(self):
        for s in range(10000):
            for robot in self.robots:
                robot.step()

            print()
            print()
            print(f"Step {s}")
            if self.check_grid():
                self.print_grid()
                print("cat")

        ans = 1
        for quadrant in range(1, 5):
            r = [robot for robot in self.robots if robot.quadrant == quadrant]
            ans *= len(r)
        return ans


class Robot:
    def __init__(self, start_pos: Point, v: Point):
        self.pos = start_pos
        self.v = v
        self.cols = COLS
        self.rows = ROWS
        self.quadrant = 0

        self.calc_quadrant()

    def step(self):
        self.pos += self.v
        new_x = self.pos.x % self.cols
        new_y = self.pos.y % self.rows
        self.pos = Point(new_x, new_y)

        self.calc_quadrant()

    def calc_quadrant(self):
        # 1,2,3,4 NW, NE, SE, SW
        match (self.pos.x, self.pos.y):
            case (x, _) if x == math.floor(self.cols / 2):
                self.quadrant = 0
            case (_, y) if y == math.floor(self.rows / 2):
                self.quadrant = 0
            case (x, y) if x < self.cols / 2 and y < self.rows / 2:
                # NW
                self.quadrant = 1
            case (x, y) if x > self.cols / 2 and y < self.rows / 2:
                # NE
                self.quadrant = 2
            case (x, y) if x > self.cols / 2 and y > self.rows / 2:
                # SW
                self.quadrant = 3
            case (x, y) if x < self.cols / 2 and y > self.rows / 2:
                # SE
                self.quadrant = 4


example_content = read_input(locations.example_file)
example_cl = example_content.split("\n")
example_cl = example_cl[3:-4]

content = read_input(locations.input_file)
cl = content.split("\n")


@timer
def part1(input):
    g = Grid(input)

    return f"{g.part_one()}"


@timer
def part2(input):
    g = Grid(input)

    # return f"{g.part_two()}"


"""
print("------------------------------------------------------------")
print("EXAMPLE INPUT")
print("------------------------------------------------------------")
example_input = example_cl
print(part1(example_input))
print()
print(part2(example_input))
"""

print()
print()
print("------------------------------------------------------------")
print("REAL INPUT")
print("------------------------------------------------------------")
input = cl
print(part1(input))
print()
print(part2(input))
