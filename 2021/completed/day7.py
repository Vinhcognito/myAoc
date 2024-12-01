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
logger_enable(log, "day7")

DAY = 7

locations = get_locations(f"day{DAY}")


#content = read_input(locations.example_file)
content = read_input(locations.input_file)

cl = content.split("\n")
inputs = ints(cl[0])[0]

crabs = sorted(inputs)

def offset_list(li:list[int], center:int) -> list:
    """refactors the list, so that every value is adjusted to the distance it is from the center value"""
    result = []
    for v in li:
        result.append(abs(v-center))
    return result

diffs = []

for i in range(crabs[0],crabs[-1]):
    diffs.append(sum(offset_list(crabs, i)))

print(f" Part1 = {min(diffs)}")

print(crabs)
# Part 2

def offset_list_p2(li:list[int], center:int) -> list:
    result = []
    for v in li:
        result.append(crab_dist(v,center))
    return result

def crab_dist(start:int, end:int) ->int:
    n = abs(start-end) + 1
    #log.debug(f"{start} -> {end} : {int(float(n/2) *(n-1))}")
    return int(float(n/2) *(n-1))

diffs = []

for i in range(crabs[0],crabs[-1]):
    diffs.append(sum(offset_list_p2(crabs, i)))


print(diffs)
print(f" Part2 = {min(diffs)}")