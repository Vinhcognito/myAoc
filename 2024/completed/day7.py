import itertools
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
from functools import reduce
from pprint import pprint

from shared.decorators import timer
from shared.helpers import Grid, Point, Vectors, get_locations, read_input
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
logger_enable(log, "7")

DAY = 7

locations = get_locations(f"day{DAY}")


# content = read_input(locations.example_file)
content = read_input(locations.input_file)

cl = content.split("\n")


class Equation:
    def __init__(self, input: str):
        self.input = input
        self.int_li = ints(input)[0]

        self.v = self.int_li[0]
        self.li = self.int_li[1:]

        self.valid: bool = False

    def test_ops(self):
        for perm in [
            "".join(p) for p in itertools.product("01", repeat=len(self.li) - 1)
        ]:
            if self.equate(perm):
                self.valid = True
                return True
        return False

    def equate(self, perm_str: str) -> bool:
        sum = self.li[0]
        for i, c in enumerate(perm_str):
            if c == "0":
                sum += self.li[i + 1]
            else:
                sum *= self.li[i + 1]

        if sum == self.v:
            return True
        return False

    def test_ops2(self):
        if self.v == 7290:
            print("stop")
        for perm in [
            "".join(p) for p in itertools.product("012", repeat=len(self.li) - 1)
        ]:
            if self.equate2(perm):
                self.valid = True
                return True
        return False

    def equate2(self, perm_str: str) -> bool:
        sum = self.li[0]
        for i, c in enumerate(perm_str):
            if c == "0":
                sum += self.li[i + 1]
            elif c == "1":
                sum *= self.li[i + 1]
            else:
                sum = int(str(sum) + str(self.li[i + 1]))

        if sum == self.v:
            return True
        return False


@timer
def part1():
    sum = 0
    for line in cl:
        equ = Equation(line)
        if equ.test_ops():
            sum += equ.v

    print(f"part1 sum: {sum}")


@timer
def part2():
    sum = 0
    for line in cl:
        equ = Equation(line)
        if equ.test_ops2():
            sum += equ.v
    print(f"part2 sum: {sum}")


part1()
part2()
