import math
import re
from collections import Counter
from dataclasses import dataclass, field
from functools import reduce
from pprint import pprint

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
    sign,
    strs,
    wait_for_input,
)

DAY = 5
print("cat")
logger_init()
logger_enable(log, f"{DAY}5")
locations = get_locations(f"day{DAY}")


content = read_input(locations.example_file)
# content = read_input(locations.input_file)


class Grid:
    def __init__(self):
        self.grid = Counter()

    def add_line(self, li: list[int], part1=True):
        x1, y1, x2, y2 = li[0:4]
        # log.debug(f"x1:{x1},y1:{y1},x2:{x2},y2:{y2}")

        # if vert or horizontal
        if x1 == x2:
            while y1 != y2:
                self.add_vent(x1, y1)
                y1 += sign(y2 - y1)
            self.add_vent(x1, y2)

        elif y1 == y2:
            while x1 != x2:
                self.add_vent(x1, y1)
                x1 += sign(x2 - x1)
            self.add_vent(x2, y2)

        else:
            # if diagonal
            if part1:
                pass
            else:
                while y1 != y2:
                    self.add_vent(x1, y1)
                    x1 += sign(x2 - x1)
                    y1 += sign(y2 - y1)
                self.add_vent(x2, y2)

    def add_vent(self, x: int, y: int):
        self.grid[Point(x, y)] += 1

    def get_overlap_vents(self):
        result_list = [key for key, value in self.grid.items() if value >= 2]
        return result_list


p1 = Point(3, 1)
p2 = Point.origin

cl = content.split("\n")

"""part1
grid = Grid()
for line in cl:
    print(ints(line)[0])
    grid.add_line(ints(line)[0])
    # pprint(grid.grid.items())

print(f"Part1: {len(grid.get_overlap_vents())}")
"""

# part2

grid = Grid()
for line in cl:
    # print(ints(line)[0])
    grid.add_line(ints(line)[0], part1=False)
    pprint(grid.grid.items())

print(f"Part2: {len(grid.get_overlap_vents())}")
print("cat")
