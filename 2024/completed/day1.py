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
logger_enable(log, "day1")


DAY = 1

locations = get_locations(f"day{DAY}")

# content = read_input(locations.example_file)
content = read_input(locations.input_file)

cl = content.split("\n")

left = []
right = []
for line in cl:
    left.append(ints(line)[0][0])
    right.append(ints(line)[0][1])

lefts = sorted(left)
rights = sorted(right)

sum = 0

for i, v in enumerate(lefts):
    sum += abs(lefts[i] - rights[i])
print(f"Part1: {sum}")

# part 2


@timer
def part2():
    left = []
    right = Counter()

    for line in cl:
        left.append(ints(line)[0][0])
        right[ints(line)[0][1]] += 1

    sum = 0

    for n in lefts:
        sum += n * right[n]

    print(f"Part2: {sum}")


part2()
