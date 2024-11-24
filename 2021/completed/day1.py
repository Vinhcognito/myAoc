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
    log,
    logger_config,
    logger_enable,
    logger_init,
    print_array,
    wait_for_input,
)

logger_init()
logger_enable(log, "day1")

DAY = 1

locations = get_locations(f"day{DAY}")


# content = read_input(locations.example_file)
# content = read_input(locations.input_file)
"""


count = 0
prev = cl[0]
# print(f"first number is {prev}")
for line in cl[1:]:
    # log.debug(f"{line} ({line>prev})")
    if line > prev:
        count += 1
    prev = line

print(count)
"""

### part 2


# content = read_input(locations.example_file)
content = read_input(locations.input_file)
cl = content.split("\n")


def sum(n):
    result = int(cl[n]) + int(cl[n + 1]) + int(cl[n + 2])
    return result


count = 0
for i, line in enumerate(cl[:-2]):
    if i == 0:
        # log.info(sum(0))
        continue
    # log.info(f"{sum(i)}, {sum(i) > sum(i - 1)}")
    if sum(i) > sum(i - 1):
        count += 1

print(count)
