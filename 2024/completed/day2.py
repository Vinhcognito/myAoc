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
    sign,
    strs,
    wait_for_input,
)

logger_init()
logger_enable(log, "2")


DAY = 2

locations = get_locations(f"day{DAY}")

# content = read_input(locations.example_file)
content = read_input(locations.input_file)

cl = content.split("\n")


def is_posneg(li: list):
    return li == sorted(li) or li[::-1] == sorted(li)


def is_within_range(li: list):
    for i in range(1, len(li)):
        if 1 <= abs(li[i] - li[i - 1]) <= 3:
            continue
        else:
            return False
    return True


def is_safe(li):
    return is_posneg(li) and is_within_range(li)


count = 0
for line in cl:
    values = ints(line)[0]
    if is_safe(values):
        count += 1


print(count)

count = 0
for line in cl:
    values = ints(line)[0]

    hit = False

    # check every possible sequence that drops one value
    for i in range(len(values)):
        if is_safe(values[:i] + values[i + 1 :]):
            hit = True

    if hit:
        count += 1

print(count)
