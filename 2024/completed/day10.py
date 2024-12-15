from __future__ import annotations

import enum
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from functools import reduce
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

DAY = 10

logger_init()
logger_enable(log, f"day{DAY}")

locations = get_locations(f"day{DAY}")


example_content = read_input(locations.example_file)
example_cl = example_content.split("\n")

content = read_input(locations.input_file)
cl = content.split("\n")


class Map:
    N = Point(0, -1)
    E = Point(1, 0)
    S = Point(0, 1)
    W = Point(-1, 0)
    dirs = [N, E, S, W]

    def __init__(self, input: list[str]):
        self.input = input

        self.g: dict[Point:int] = defaultdict(int)
        self.trailheads: list[Trail] = []
        self.rows: int = len(input)
        self.cols: int = len(input[0])

        for col, line in enumerate(input):
            for row, n in enumerate(line):
                _p = Point(col, row)
                self.g[_p] = int(n)
                if n == "0":
                    self.trailheads.append(Trail(_p))

    def part_one(self):
        for th in self.trailheads:
            self.check_trailhead(th)

    def part_two(self):
        for th in self.trailheads:
            self.check_trailhead_p2(th)

    def check_trailhead(self, trail: Trail):
        to_check: list[Point] = []
        checked: set[Point] = set()

        to_check = self._find_valid_neighbours(trail.p)
        while len(to_check) > 0:
            current = to_check.pop(-1)
            if current in checked:
                continue
            checked.add(current)

            if self.g[current] == 9:
                trail.score += 1
            to_check.extend(self._find_valid_neighbours(current))

    def check_trailhead_p2(self, trail: Trail):
        to_check: list[Point] = []

        to_check = self._find_valid_neighbours(trail.p)
        while len(to_check) > 0:
            current = to_check.pop(-1)

            if self.g[current] == 9:
                trail.score += 1
            to_check.extend(self._find_valid_neighbours(current))

    def _find_valid_neighbours(self, p: Point):
        """gets list of points that surround this point that are valid for the next step in the trail"""
        return [p + vec for vec in Map.dirs if self.g.get((p + vec)) == self.g[p] + 1]

    def score_part1(self):
        sum = 0
        for th in self.trailheads:
            sum += th.score
        print(f"The Score is: {sum}")

    def __str__(self):
        listmap: list[list[int]] = [
            [0 for c in range(self.rows)] for r in range(self.cols)
        ]

        p: Point
        value: str
        for p, value in self.g.items():
            listmap[p.col][p.row] = str(value)

        listmap_str = ""
        for line in listmap:
            listmap_str += "".join(line)
            listmap_str += "\n"
        return listmap_str


class Trail:
    def __init__(self, point: Point):
        self.p = point
        self.score: int = 0


@timer
def part1(input):
    m = Map(input)
    m.part_one()
    m.score_part1()


@timer
def part2(input):
    m = Map(input)
    m.part_two()
    m.score_part1()


example_input = example_cl
print("\n==========Example Inputs===========\n")
part1(example_input)
part2(example_input)


print("\n==========Real Inputs============\n")
input = cl
part1(input)
part2(input)
