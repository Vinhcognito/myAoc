import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from functools import reduce
from itertools import combinations
from pprint import pprint

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

logger_init()
logger_enable(log, "8")

DAY = 8

locations = get_locations(f"day{DAY}")


# content = read_input(locations.example_file)
content = read_input(locations.input_file)


class Grid:
    def __init__(self, content: str):
        self.content = content
        self.cl = content.split("\n")
        self.rows = len(self.cl)
        self.cols = len(self.cl[0])

        self.d: dict[Point:str] = defaultdict(str)

        self.nodes = set()

        for row, line in enumerate(self.cl):
            for col, c in enumerate(line):
                if c != ".":
                    self.d[Point(col, row)] = c

    def get_all_combinations(self, li: list):
        """find all combinations for this antenna signal"""
        return list(combinations(li, 2))

    def get_valid_antinodes(self, p1: Point, p2: Point) -> int:
        """0, 1 or 2 antinodes from the two points"""
        a1 = p2 + (p2 - p1)
        a2 = p1 + (p1 - p2)

        # check if in bounds
        result = 0

        if (0 <= a1.row < self.rows) and (0 <= a1.col < self.cols):
            self.nodes.add(a1)
        if (0 <= a2.row < self.rows) and (0 <= a2.col < self.cols):
            self.nodes.add(a2)

        return result

    def group_keys_by_signal(self):
        grouped = defaultdict(list)
        for key, value in self.d.items():
            grouped[value].append(key)
        return dict(grouped)

    @timer
    def part_one(self):
        grouped = self.group_keys_by_signal()

        for key, value in grouped.items():
            combs = self.get_all_combinations(value)
            for pair in combs:
                self.get_valid_antinodes(*pair)

        print(f"Part 1: {len(self.nodes)}")


grid = Grid(content)
grid.part_one()
