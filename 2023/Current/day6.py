from collections import Counter
from dataclasses import dataclass, field
from functools import reduce
from math import ceil, sqrt
from pprint import pprint  # noqa: F401

from helpers import Grid, Point, get_locations, read_input  # noqa: F401
from loguru import logger  # noqa: F401
from util import (  # noqa: F401
    clear_terminal,
    extend_list,
    extend_list_2D,
    extend_list_rect,
    logger_config,
    print_array,
)

DAY = 6

locations = get_locations(f"day{DAY}")
logger.add(f"{locations.log_file}", backtrace=True, diagnose=True)
logger_config(logger)
clear_terminal()

content = read_input(locations.input_file)
cl = content.split("\n")


@dataclass
class Race:
    time: int
    record: int
    part: int
    results: list[int] = field(default_factory=list)
    result_counter: Counter = field(default_factory=Counter)
    winning_options: int = 0
    # for part 2
    c1: float = 0
    c2: float = 0

    def __post_init__(self):
        if self.part == 1:
            self.gen_results_list()
        else:
            self.c1 = (self.time + sqrt(self.time**2 - 4 * self.record)) / 2
            self.c2 = (self.time - sqrt(self.time**2 - 4 * self.record)) / 2
            self.calc_race_fast()

    def gen_results_list(self):
        """slow"""
        for i in range(self.time + 1):
            result = self.calc_race_slow(i)
            self.results.append(result)
            self.result_counter[result] += 1
            if result > self.record:
                self.winning_options += 1

    def calc_race_slow(self, charge):
        #  d = ct - c^2  or
        #  d = -c(c-t)
        # distance = -charge * (charge - self.time)
        distance = (charge * self.time) - charge**2
        return distance

    def calc_race_fast(self):
        # d = ct-c^2
        # c^2 - ct + d = 0
        # c = [t ± sqrt((t)^2 - 4*1*d)] / (2*1)
        self.winning_options = ceil(self.c1) - ceil(self.c2)


# get times and records
times = [int(element) for element in cl[0].split()[1:]]
records = [int(element) for element in cl[1].split()[1:]]

races = [Race(time, record, part=1) for time, record in zip(times, records)]

# extract all winning options
winning_options = [race.winning_options for race in races]

# calculate the product of this list
product = reduce((lambda x, y: x * y), winning_options)

print(f"Part 1: product of winning options = {product}")

# part 2
time = "".join(map(str, times))
record = "".join(map(str, records))
race = Race(int(time), int(record), part=2)
print(f"Part2: # of winning options = {race.winning_options}")
