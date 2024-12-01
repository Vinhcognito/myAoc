import math
import re
from collections import Counter, defaultdict
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
logger_enable(log, "day6")

DAY = 6

locations = get_locations(f"day{DAY}")


# content = read_input(locations.example_file)
content = read_input(locations.input_file)

cl = content.split("\n")
for line in cl:
    inputs = ints(line)[0]

ex = [5, 6, 7, 9, 10, 10, 10, 10, 11, 12, 15, 17, 19, 20, 20, 21, 22, 26]


class FishTracker:
    fish = [0] * 9

    def __init__(self, li: list[int]):
        for f in li:
            self.fish[f] += 1

    def count_fish(self):
        return sum(self.fish[0:9])

    def increment_day(self):
        birthingfish = self.fish.pop(0)
        self.fish[6] += birthingfish
        self.fish.append(birthingfish)


tracker = FishTracker(inputs)


for day in range(1, 257):
    tracker.increment_day()
    if day <= 18:
        log.info(f"Part 1: day:{day}, #: {tracker.count_fish()}, answer:{ex[day-1]}")
    else:
        log.info(f"Part 2: day:{day}, #: {tracker.count_fish()}")
