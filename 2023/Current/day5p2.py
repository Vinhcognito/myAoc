import copy
from dataclasses import dataclass
from operator import add, sub
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

content = read_input(locations.input_file)
cl = content.split("\n")


@dataclass
class Rng:
    start: int
    stop: int
    tier: int


def range_intersection(rng1, rng2):
    if rng1[0] < rng2[1] and rng1[1] > rng2[0]:
        intersection_start = max(rng1[0], rng2[0])
        intersection_end = min(rng1[1], rng2[1])
        return (intersection_start, intersection_end)
    else:
        return None


def tuple_add(tup, num):
    """returns (tup[0]+num, tup[1]+num)"""
    return tuple(map(add, tup, (num, num)))


def get_mapped_rngs(rng, map_dict: list):
    """given a range and a tier of mappings, return a list of the converted ranges, split if need be"""
    converted_results = []
    unconverted_splits = []
    hasMatch = False

    for map in map_dict.keys():
        offset = map_dict[map]

        intersection = range_intersection(rng, map)
        if intersection is not None:
            rng_min = rng[0]
            rng_max = rng[1]
            int_min = intersection[0]
            int_max = intersection[1]

            match (rng_min >= int_min), (rng_max <= int_max):
                case True, True:
                    #   [---]
                    #  [======]
                    # append the rng, converted from src to dest
                    converted_results.append(tuple_add(rng, offset))
                    hasMatch = True
                case False, False:
                    # [------]
                    #   [==]
                    unconverted_splits.append((rng_min, int_min))
                    converted_results.append(tuple_add(intersection, offset))
                    unconverted_splits.append((int_max, rng_max))
                    hasMatch = True
                case True, False:
                    #   [---]
                    # [===]
                    converted_results.append(tuple_add((rng_min, int_max), offset))
                    unconverted_splits.append((int_max, rng_max))
                    hasMatch = True
                case False, True:
                    # [---]
                    #   [===]
                    unconverted_splits.append((rng_min, int_min))
                    converted_results.append(tuple_add((int_min, rng_max), offset))
                    hasMatch = True

    if not hasMatch:
        # logger.critical(f"returning:{rng}")
        if isinstance(rng, tuple):
            return [rng]
        if isinstance(rng, list):
            return rng
    else:
        for unconverted_map in unconverted_splits:
            result = get_mapped_rngs_splits(unconverted_map, map_dict)
            # logger.critical(result)
            # logger.critical(f"converted_results:{converted_results}")
            if result is not None:
                converted_results.extend(result)
            # logger.critical(f"returning:{converted_results}")

        if isinstance(converted_results, tuple):
            return [converted_results]
        if isinstance(converted_results, list):
            return converted_results


def get_mapped_rngs_splits(rng, map_dict: list):
    """given a range and a tier of mappings, return a list of the converted ranges, split if need be"""

    converted_results = []
    unconverted_splits = []
    hasMatch = False

    for map in map_dict.keys():
        offset = map_dict[map]

        intersection = range_intersection(rng, map)
        if intersection is not None:
            rng_min = rng[0]
            rng_max = rng[1]
            int_min = intersection[0]
            int_max = intersection[1]

            match (rng_min >= int_min), (rng_max <= int_max):
                case True, True:
                    #   [---]
                    #  [======]
                    # append the rng, converted from src to dest
                    converted_results.append(tuple_add(rng, offset))
                    hasMatch = True
                case False, False:
                    # [------]
                    #   [==]
                    unconverted_splits.append((rng_min, int_min))
                    converted_results.append(tuple_add(intersection, offset))
                    unconverted_splits.append((int_max, rng_max))
                    hasMatch = True
                case True, False:
                    #   [---]
                    # [===]
                    converted_results.append(tuple_add((rng_min, int_max), offset))
                    unconverted_splits.append((int_max, rng_max))
                    hasMatch = True
                case False, True:
                    # [---]
                    #   [===]
                    unconverted_splits.append((rng_min, int_min))
                    converted_results.append(tuple_add((int_min, rng_max), offset))
                    hasMatch = True

    # if no matches at all return unchanged
    if not hasMatch:
        # logger.critical(f"splits returning:{rng}")
        if isinstance(rng, tuple):
            return [rng]
        if isinstance(rng, list):
            return rng
    else:
        # all unconverted splits have no match
        # -> return unchanged
        if len(unconverted_splits) > 0:
            # logger.critical(f"unconverted_splits:{unconverted_splits}")
            converted_results.extend(unconverted_splits)
        # logger.critical(f"splits returning:{converted_results}")
        if isinstance(converted_results, tuple):
            return [converted_results]
        if isinstance(converted_results, list):
            return converted_results


### Part 2
seeds = []
mappings = [None, {}, {}, {}, {}, {}, {}, {}, {}]
mapping_tier = -1

# convert seeds into intervals (start,end) - (inc,exc)
# convert mappings into intervals (src_start,src_end):(dest-src)
# so that src + (dest-src) = dest

for line in cl:
    # parse input for seeds and mappings
    split = line.split(":")
    if len(split) > 1:
        if mapping_tier == -1:
            li = ints(split[1])[0]
            seeds = [(li[i], li[i] + li[i + 1]) for i in range(0, len(li) - 1, 2)]
        mapping_tier += 1
    else:
        li = ints(split[0])[0]
        if len(li) == 3:
            dest, src, maprange = li
            mappings[mapping_tier][(src, src + maprange)] = dest - src

locations = []
soils = []
for seed in seeds:
    soils.extend(get_mapped_rngs(seed, mappings[1]))

# logger.critical("====================================================")
# logger.info(f"seeds{seeds}")
# logger.success(mappings[1])
soils = []
for seed in seeds:
    soils.extend(get_mapped_rngs(seed, mappings[1]))

rngs = [None, copy.deepcopy(seeds), copy.deepcopy(soils)]
for i in range(2, len(mappings)):
    # logger.info(rngs[i])
    # logger.success(mappings[i])
    rngs.append([])
    for rng in rngs[i]:
        rngs[i + 1].extend(get_mapped_rngs(rng, mappings[i]))

min_location = min(rngs[8], key=lambda x: x[0])
print(f"Part 2\nLowest location: {min_location} ")
