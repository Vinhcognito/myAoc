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

DAY = 11

logger_init()
logger_enable(log, f"day{DAY}")

locations = get_locations(f"day{DAY}")

example_content = read_input(locations.example_file)
example_cl = example_content.split("\n")
# example_cl = example_cl[3:-4]

content = read_input(locations.input_file)
cl = content.split("\n")


class Stones:
    def __init__(self, input: str):
        self.transforms: dict[int : [list[int]]] = {}

        input_int = list(map(int, input.split(" ")))
        self.stones: Counter[int:int] = Counter(input_int)

    def _calc_blink(self, stone_value: int) -> list[int]:
        """ "returns output of this stone after a blink"""
        if stone_value in self.transforms.keys():
            return self.transforms[stone_value]
        else:
            # 0 => 1
            if stone_value == 0:
                return [1]
            # even number of digits => split into 2
            if len(str(stone_value)) % 2 == 0:
                s = str(stone_value)
                midpoint = int(len(s) / 2)
                return [int(s[:midpoint]), int(s[midpoint:])]
            # default, *= 2024
            return [stone_value * 2024]

    def count_stones_after_blinks(self, blinks: int):
        # calc blink for each stone in self.stones

        for i in range(blinks):
            print(f"on blink# {i}")
            new_counter = Counter()
            stone_copy = self.stones.items()
            for stone_value, quantity in stone_copy:
                if quantity == 0:
                    continue
                transformation_list = self._calc_blink(stone_value)

                for sv in transformation_list:
                    new_counter[sv] += quantity

            self.stones = new_counter
            # self._print_stones()
        return self.stones.total()

    def _print_stones(self):
        print([_ for _ in self.stones.elements()])


@timer
def part1(input):
    s = Stones(input)
    return s.count_stones_after_blinks(25)


@timer
def part2(input):
    s = Stones(input)
    return s.count_stones_after_blinks(75)


print("------------------------------------------------------------")
print("EXAMPLE INPUT")
print("------------------------------------------------------------")
example_input = example_content
print(part1(example_input))
print()
print(part2(example_input))

print()
print()
print("------------------------------------------------------------")
print("REAL INPUT")
print("------------------------------------------------------------")
input = content
print(part1(input))
print()
print(part2(input))
