from __future__ import annotations

import copy
from audioop import lin2adpcm
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
)

DAY = 14

locations = get_locations(f"day{DAY}")
# logger.add(f"{locations.log_file}", backtrace=True, diagnose=True)
logger_config(logger)
clear_terminal()

content = read_input(locations.input_file)
rows = content.split("\n")
grid_width = len(rows[0])
grid_height = len(rows)


class Rock:
    rocks: dict[Point, Rock] = {}
    grid: dict[Point, str] = {}
    cycle: list[Point] = [Vectors.N, Vectors.W, Vectors.S, Vectors.E]
    prev_rock_list = []

    def __init__(self, point: Point):
        self.point = point
        self.count: int = 0

    def isWithinBounds(self, dir_vector: Point):
        return (
            0 <= self.point.x + dir_vector.x < grid_width
            and 0 <= self.point.y + dir_vector.y < grid_height
        )

    def move(self, dir_vector: Point):
        start_point = self.point
        while True:
            if self.isWithinBounds(dir_vector):
                # check if blocked by #
                if self.point + dir_vector in self.grid:
                    break
                # check if blocked by O rock
                elif self.point + dir_vector in self.rocks:
                    break
                else:
                    self.point += dir_vector
            else:
                break
        # if rock has moved
        if self.point != start_point:
            Rock.rocks[self.point] = self
            del Rock.rocks[start_point]
            self.count = 0
        else:
            self.count += 1
        # if rock is stuck remove from list of movable rocks
        if self.count == 4:
            logger.critical(f"{self.point} is locked")
            self.locked()

    @staticmethod
    def sorted_rocks(dir_vector: Point) -> list[Rock]:
        match dir_vector:
            case Vectors.N:
                li = list(Rock.rocks.values())
                li.sort(key=lambda rock: rock.point.y)
                return li
            case Vectors.S:
                li = list(Rock.rocks.values())
                li.sort(key=lambda rock: rock.point.y, reverse=True)
                return li
            case Vectors.W:
                li = list(Rock.rocks.values())
                li.sort(key=lambda rock: rock.point.x)
                return li
            case Vectors.E:
                li = list(Rock.rocks.values())
                li.sort(key=lambda rock: rock.point.x, reverse=True)
                return li

    @staticmethod
    def tilt_grid(dir_vector: Point):
        for rock in Rock.sorted_rocks(dir_vector):
            rock.move(dir_vector)

    @staticmethod
    def tilt_cycle():
        for dir in Rock.cycle:
            Rock.tilt_grid(dir)

    def locked(self):
        Rock.grid[self.point] = "O"
        del Rock.rocks[self.point]

    @staticmethod
    def calculate_load() -> int:
        load = 0
        for point in Rock.grid.keys():
            if Rock.grid[point] == "O":
                load += grid_height - point.y

        for rock in Rock.rocks.values():
            load += grid_height - rock.point.y

        return load

    @staticmethod
    def get_grid_string() -> str:
        rocks = list(Rock.rocks.keys())
        rocks.extend(list(Rock.grid.keys()))
        rocks.sort(key=lambda point: (point.x, point.y))
        output = ""
        for point in rocks:
            if point in Rock.rocks:
                c = "O"
            else:
                c = "#"
            output += f"{str(point)}{c}"
        return output


# parse input
for y, row in enumerate(rows):
    for x, c in enumerate(row):
        if c == "O":
            Rock.rocks[Point(x, y)] = Rock(Point(x, y))
        if c == "#":
            Rock.grid[Point(x, y)] = c

# Part 2
cycles = 1000000000 + 1
results = {}
cycle_length = 0
i = 1

while True:
    Rock.tilt_cycle()
    s = Rock.get_grid_string()
    if s in results:
        cycle_length = i - results[s]
        for idx in results.values():
            if idx >= results[s] and idx % cycle_length == cycles % cycle_length:
                print(f"part 2 load: {Rock.calculate_load()}")
        break
    results[s] = i
    i += 1
