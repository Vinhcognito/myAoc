from __future__ import annotations

import enum
import math
import re
from collections import Counter, defaultdict
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

DAY = 12

logger_init()
logger_enable(log, f"day{DAY}")

locations = get_locations(f"day{DAY}")

N = Point(0, -1)
E = Point(1, 0)
S = Point(0, 1)
W = Point(-1, 0)
dirs = [N, E, S, W]


def get_neighbours(point: Point) -> list[Point]:
    return [point + vec for vec in dirs]


class Farm:
    def __init__(self, input: list[str]):
        self.land: dict[Point:str] = {}
        self.rows = len(input)
        self.cols = len(input[0])
        self.plants: list[Plant] = []

        for row, line in enumerate(input):
            for col, p in enumerate(line):
                self.land[Point(col, row)] = p

    def part_one(self):
        self._parse_plants()
        return self.part_one_price()

    def part_one_price(self):
        return sum([plant.total_price for plant in self.plants])

    def _parse_plants(self):
        for value in set(self.land.values()):
            p = Plant(value, [k for k, v in self.land.items() if v == value])
            self.plants.append(p)

    def part_two(self):
        self._parse_plants()
        return self.part_two_price()

    def part_two_price(self):
        return sum([plant.total_price2 for plant in self.plants])


class Plant:
    def __init__(self, name: str, input: list[Point]):
        self.name: str = name
        self.points: list[Point] = input
        self.regions: list[Region] = []
        self._find_regions()

        self.total_price: int = sum([region.price for region in self.regions])

        self.total_price2: int = sum([region.price2 for region in self.regions])

    def _find_regions(self):
        points_to_check = [p for p in self.points]
        checked: list[Point] = []
        region_list = []

        while len(points_to_check) > 0:
            p = points_to_check.pop(-1)
            checked.append(p)

            valid_neighbours = self._get_valid_n(p)
            _region = [p]

            while len(valid_neighbours) > 0:
                valid_n = valid_neighbours.pop(-1)

                if valid_n not in checked:
                    points_to_check.remove(valid_n)
                    checked.append(valid_n)

                    _region.append(valid_n)
                    valid_neighbours.extend(self._get_valid_n(valid_n))

            region_list.append(_region)

        for region in region_list:
            self.regions.append(Region(region))

    def _get_valid_n(self, point: Point) -> list[Point]:
        neighbours = get_neighbours(point)
        valid_neighbours = list(set(neighbours).intersection(self.points))
        return valid_neighbours


class Region:
    def __init__(self, input: list[Point]):
        self.points: list[Point] = input
        self.area: int = len(self.points)
        self.perimeter: int = self._calc_perimeter()
        self.price: int = self.area * self.perimeter
        self.edges: int = self._calc_edges()
        self.price2: int = self.area * self.edges

    def _calc_perimeter(self) -> int:
        perimeter = self.area * 4
        for p in self.points:
            perimeter -= len(set(self.points).intersection(set(get_neighbours(p))))

        return perimeter

    def _calc_edges(self) -> int:
        NE = [N, E]
        NW = [N, W]
        SE = [S, E]
        SW = [S, W]
        corners = [NE, NW, SE, SW]

        number_of_corners = 0
        for point in self.points:
            for corner in corners:
                points_to_check = [point + corner[0], point + corner[1]]
                # check for inner corners
                if (
                    points_to_check[0] in self.points
                    and points_to_check[1] in self.points
                ):
                    # check point diagonal to this corner
                    if (point + corner[0] + corner[1]) not in self.points:
                        number_of_corners += 1

                # check for outer corners
                if (points_to_check[0] not in self.points) and (
                    points_to_check[1] not in self.points
                ):
                    number_of_corners += 1

        return number_of_corners


example_content = read_input(locations.example_file)
example_cl = example_content.split("\n")
# example_cl = example_cl[3:-4]

content = read_input(locations.input_file)
cl = content.split("\n")


@timer
def part1(input):
    f = Farm(input)

    return f"{f.part_one()}"


@timer
def part2(input):
    f = Farm(input)

    return f"{f.part_two()}"


print("------------------------------------------------------------")
print("EXAMPLE INPUT")
print("------------------------------------------------------------")
example_input = example_cl
print(part1(example_input))
print()
print(part2(example_input))

print()
print()
print("------------------------------------------------------------")
print("REAL INPUT")
print("------------------------------------------------------------")
input = cl
print(part1(input))
print()
print(part2(input))
