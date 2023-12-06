import copy
from pprint import pprint  # noqa: F401

from decorators import timer  # noqa:F401
from helpers import Grid, Point, get_locations, read_input  # noqa: F401
from loguru import logger  # noqa: F401
from util import (  # noqa: F401
    clear_terminal,
    extend_list,
    extend_list_2D,
    extend_list_rect,
    ints,
    logger_config,
    print_array,
    wait_for_input,
)

DAY = 5

locations = get_locations(f"day{DAY}")
logger.add(f"{locations.log_file}", backtrace=True, diagnose=True)
logger_config(logger)
clear_terminal()

content = read_input(locations.example_file)
cl = content.split("\n")


### part 1
sum = 0
seeds = []
part2_seeds = []
mappings = [None, [], [], [], [], [], [], [], []]
mapping_tier = -1


def get_map_value(value, mapping_list: list):
    """if value is in source maprange, returns corresponding value
    else returns value"""
    for map in mapping_list:
        dest, source, maprange = map
        if value >= source and value < source + maprange:
            return value + (dest - source)
    return value


### Part 1

for line in cl:
    # parse input for all mappings
    split = line.split(":")
    if len(split) > 1:
        if mapping_tier == -1:
            seeds = ints(split[1])[0]
        mapping_tier += 1
    else:
        numbers = ints(split[0])[0]
        if len(numbers) == 3:
            mappings[mapping_tier].append(numbers)

locations = []

for seed in seeds:
    locations.append(copy.copy(seed))
    for i in range(1, len(mappings)):
        seed = get_map_value(seed, mappings[i])

    locations.append((locations.pop(), seed))

min_location, min_seed = min(locations, key=lambda tup: tup[1])
print(f"Part 1\nLowest location: {min_location} " + f"seed: {min_seed}")
