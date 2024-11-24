import math
import re
from collections import Counter
from dataclasses import dataclass, field
from functools import reduce
from pprint import pprint

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
logger_enable(log, "day1")

DAY = 3

locations = get_locations(f"day{DAY}")


# content = read_input(locations.example_file)
content = read_input(locations.input_file)

cl = content.split("\n")


def part_one():
    count = Counter()
    rows = len(cl)

    # count the bits
    for line in cl:
        for i, v in enumerate(line):
            if int(v) == 1:
                count[i] += 1

    # iterate through bits and construct the binary
    _gamma = []
    _epsilon = []
    for bit in sorted(count.items(), key=lambda x: x[0]):
        if bit[1] > rows / 2:
            _gamma.append("1")
            _epsilon.append("0")
        else:
            _gamma.append("0")
            _epsilon.append("1")

    gamma = int("".join(_gamma), 2)
    epsilon = int("".join(_epsilon), 2)
    power = gamma * epsilon

    print(f"Part 1: Power = gamma:{gamma} * epsilon:{epsilon} = {power}")


# part_one()


# count the bits
def count_bits(bit: int, li: list):
    ones = []
    zeroes = []
    count = 0

    for line in li:
        if int(line[bit]) == 1:
            count += 1
            ones.append(line)
        else:
            count -= 1
            zeroes.append(line)

    return (count, ones, zeroes)


# eliminate
def eliminate(count: int, ones_list: list, zeroes_list: list, o2=True):
    o2_remain = []
    co2_remain = []
    if count >= 0:
        o2_remain.extend(ones_list)
        co2_remain.extend(zeroes_list)
    else:
        o2_remain.extend(zeroes_list)
        co2_remain.extend(ones_list)

    if o2:
        return o2_remain
    else:
        return co2_remain


digits = len(cl[0])

# o2
remainders = cl
for n in range(digits):
    count, ones, zeroes = count_bits(n, remainders)
    remainders = eliminate(count, ones, zeroes, True)
    if len(remainders) == 1:
        break

o2 = int(remainders[0], 2)
print(f"o2 = {o2}")

# co2
remainders = cl
for n in range(digits):
    count, ones, zeroes = count_bits(n, remainders)
    remainders = eliminate(count, ones, zeroes, False)
    if len(remainders) == 1:
        break

co2 = int(remainders[0], 2)
print(f"co2 = {co2}")

print(f"life support rating = o2: {o2} * co2: {co2} = {o2*co2}")
