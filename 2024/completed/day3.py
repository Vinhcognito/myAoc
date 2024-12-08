import math
import re
from collections import Counter
from dataclasses import dataclass, field
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
logger_enable(log, "3")

DAY = 3

locations = get_locations(f"day{DAY}")


# content = read_input(locations.example_file)
content = read_input(locations.input_file)

valid_chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ","]


class Mul:
    def __init__(self, s: str, i: int):
        self.i = i
        self.s = s
        self.end = self.s.find(")")
        if self.end != -1:
            self.s = self.s[: self.end + 1]

    def is_valid(self) -> bool:
        if self.end == -1:
            return False

        commas = 0
        for c in self.s[4:-1]:
            if c in valid_chars:
                if c == ",":
                    commas += 1
                continue
            else:
                return False

        if commas == 1:
            return True
        else:
            return False

    def get_value(self) -> int:
        return ints(self.s)[0][0] * ints(self.s)[0][1]


def find_instances(s: str, search: str):
    indices = []
    pos = 0
    while True:
        pos = s.find(search, pos)
        if pos == -1:
            break
        indices.append(pos)
        pos += 1  # Move to the next character
    return indices


cl = content.split("\n")


@timer
def part1():
    sum = 0
    for line in cl:
        mul_str_list = find_instances(line, "mul(")
        print(mul_str_list)
        for i in mul_str_list:
            mul = Mul(line[i : i + 13])
            if mul.is_valid():
                sum += mul.get_value()

    print(f"Part1:{sum}")


part1()


# part 2


def is_active(dos: list[int], donts: list[int], target: int) -> bool:
    highest_do = max((num for num in dos if num < target), default=0)
    highest_dont = max((num for num in donts if num < target), default=0)

    if highest_do == 0 and highest_dont == 0:
        return True

    return highest_do > highest_dont


@timer
def part2():
    sum = 0

    mul_str_list = find_instances(content, "mul(")

    mul_list: list[Mul] = []

    for i in mul_str_list:
        mul = mul = Mul(content[i : i + 13], i)
        if mul.is_valid():
            mul_list.append(mul)

    do_str_list = find_instances(content, "do()")

    dont_str_list = find_instances(content, "don't()")

    for mul in mul_list:
        if is_active(do_str_list, dont_str_list, mul.i):
            sum += mul.get_value()

    print(sum)


part2()
