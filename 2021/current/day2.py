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

DAY = 2

locations = get_locations(f"day{DAY}")


# content = read_input(locations.example_file)
content = read_input(locations.input_file)

cl = content.split("\n")

# PArt 1
"""
horizontal = 0
depth = 0

for line in cl:
    if strs(line)[0] == "forward":
        horizontal += ints(line)[0][0]
        # print(f"hori:{horizontal}")
    elif strs(line)[0] == "up":
        depth -= ints(line)[0][0]
        # print(f"dep:{depth}")
    elif strs(line)[0] == "down":
        depth += ints(line)[0][0]
        # print(f"dep:{depth}")

print(f"horizontal:{horizontal} * depth:{depth} = {horizontal*depth}")
"""

# Part 2

horizontal = 0
depth = 0
aim = 0

for line in cl:
    if strs(line)[0] == "forward":
        horizontal += ints(line)[0][0]
        depth += ints(line)[0][0] * aim
    elif strs(line)[0] == "up":
        aim -= ints(line)[0][0]
    elif strs(line)[0] == "down":
        aim += ints(line)[0][0]

print(f"horizontal:{horizontal} * depth:{depth} = {horizontal*depth}")
