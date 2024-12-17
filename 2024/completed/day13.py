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

DAY = 13

logger_init()
logger_enable(log, f"day{DAY}")

locations = get_locations(f"day{DAY}")


class Games:
    def __init__(self, input: str):
        self.game_inputs = input.split("\n\n")
        self.games: list[Game] = []

    def part_one(self):
        for game in self.game_inputs:
            lines = game.split("\n")
            A = Point(ints(lines[0])[0][0], ints(lines[0])[0][1])
            B = Point(ints(lines[1])[0][0], ints(lines[1])[0][1])
            Prize = Point(ints(lines[2])[0][0], ints(lines[2])[0][1])

            self.games.append(Game(A, B, Prize))
        for game in self.games:
            game.part_one()

        return sum([g.cost for g in self.games])

    def part_two(self):
        c = 10000000000000

        for game in self.game_inputs:
            lines = game.split("\n")
            A = Point(ints(lines[0])[0][0], ints(lines[0])[0][1])
            B = Point(ints(lines[1])[0][0], ints(lines[1])[0][1])
            Prize = Point(ints(lines[2])[0][0] + c, ints(lines[2])[0][1] + c)

            self.games.append(Game(A, B, Prize))

        for game in self.games:
            game.part_two()

        return sum([g.cost for g in self.games])


class Game:
    def __init__(self, A: Point, B: Point, P: Point):
        self.a: Point = A
        self.b: Point = B
        self.p: Point = P
        self.a_count: float
        self.b_count: float

        self.cost: int = 0

        self._solve_a_count()
        self._solve_b_count()

        # print(f"a_count = {self.a_count}")
        # print(f"b_count = {self.b_count}")

    def part_one(self):
        if (
            self.is_whole_number(self.a_count)
            and self.is_whole_number(self.b_count)
            and (self.a_count <= 100)
            and (self.b_count <= 100)
        ):
            self.cost = (self.a_count * 3) + (self.b_count)

    def part_two(self):
        if self.is_whole_number(self.a_count) and self.is_whole_number(self.b_count):
            self.cost = (self.a_count * 3) + (self.b_count)

    def is_whole_number(self, n):
        return n == int(n)

    def _solve_a_count(self):
        self.a_count = ((self.p.x * self.b.y) - (self.p.y * self.b.x)) / (
            (self.a.x * self.b.y) - (self.b.x * self.a.y)
        )

    def _solve_b_count(self):
        self.b_count = (self.p.x - (self.a_count * self.a.x)) / self.b.x


example_content = read_input(locations.example_file)
example_cl = example_content.split("\n")
# example_cl = example_cl[3:-4]

content = read_input(locations.input_file)
cl = content.split("\n")


@timer
def part1(input):
    g = Games(input)

    return f"{g.part_one()}"


@timer
def part2(input):
    g = Games(input)

    return f"{g.part_two()}"


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
