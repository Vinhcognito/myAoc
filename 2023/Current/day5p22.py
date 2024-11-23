import copy
from dataclasses import dataclass
from itertools import groupby
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

content = read_input(locations.example_file)


# convert seeds into intervals (start,end) - (inc,exc)
# convert mappings into map
# offset = dest-src
# so that src + offset = dest


@dataclass
class Rng:
    start: int
    stop: int
    tier: int = 0

    def convert(self, offset):
        """indicates that this rng had a mapset checked and applied
        adds map offset to both start and stop"""

        self.start += offset
        self.stop += offset
        self.tier += 1


@dataclass(init=False)
class Map:
    start: int
    stop: int
    offset: int

    def __init__(self, dest, src, maprange):
        self.start = src
        self.stop = src + maprange
        self.offset = dest - src

    def apply_onto(self, rng: Rng) -> list[list[Rng], list[Rng]]:
        """applies map onto the rng, splitting the rng if neccessary
        outputs: [list[converted rng],list [unconverted rng]]"""
        converted = []
        unconverted = []

        intersect = self.does_rng_intersect(rng)
        if intersect is not None:
            # determine if and how to split the rng
            # based on relationship of rng and map
            # converts rng that is within map
            intersection_rng = Rng(intersect.start, intersect.stop, rng.tier)

            intersection_rng.convert(self.offset)
            converted.append(intersection_rng)

            if intersect.start > rng.start:
                # [----
                #   [==
                left_rng = Rng(rng.start, intersect.start, rng.tier)
                unconverted.append(left_rng)

            if intersect.stop < rng.stop:
                #  ----]
                #  ==]
                right_rng = Rng(intersect.stop, rng.stop, rng.tier)
                unconverted.append(right_rng)

            # logger.debug(f"converted:{converted}")
            # logger.debug(f"unconverted:{unconverted}")
            return [converted, unconverted]
        else:
            return [[], [rng]]

    def does_rng_intersect(self, rng: Rng):
        """returns rng of intersection if there is one"""
        if (rng.start < self.stop) and (rng.stop > self.start):
            intersection_start = max(self.start, rng.start)
            intersection_end = min(self.stop, rng.stop)
            return Rng(intersection_start, intersection_end, rng.tier)
        else:
            return None


class Mapset:
    """a tier of maps"""

    def __init__(self, rawstring: str, tier) -> None:
        lines = rawstring.split("\n")[1:]
        self.maps: list[Map] = []
        self.tier = tier
        for line in lines:
            s, d, r = line.split()
            self.maps.append(Map(int(s), int(d), int(r)))

    def process(self, rngs: list[Rng]):
        converted = []
        unconverted = list(filter(None, rngs))
        splits: list[Rng] = []
        # ensure map and all resulting splits are tested with every map
        for rng in unconverted:
            for i, map in enumerate(self.maps):
                # logger.warning(rng)
                # logger.warning(map)
                con_res, uncon_res = map.apply_onto(rng)
                # logger.critical(con_res)
                # logger.critical(uncon_res)
                if len(con_res) != 0:
                    # if there was a match, continue with only untested splits
                    converted.extend(con_res)
                    for split in uncon_res:
                        rng = Rng(split.start, split.stop, split.tier)
                # if at end of mapset

                # logger.warning(uncon_res)
                if i == len(self.maps) - 1:
                    splits.extend(uncon_res)
            # logger.debug(converted)
        # logger.critical(splits)
        # all remaining unconverted have no match
        for holdout in splits:
            holdout.convert(0)
            converted.append(holdout)

        return list(filter(None, converted))


cl = content.split("\n\n")
seeds, *mapstrings = cl
seeds = [int(x) for x in seeds.split(":")[1].split()]

mapsets = [Mapset(string, tier) for tier, string in enumerate(mapstrings, 1)]

# create starting rngs from seed list

ranges = [Rng(a, a + b) for a, b in zip(seeds[::2], seeds[1::2])]
logger.success(f"seeds:{ranges}")
##ranges = [Rng(93533455, 93533455 + 128569683)]
for mapset in mapsets:
    print(f"Tier:{mapset.tier}")
    # pprint(f"mapset:\n{mapset.maps}")
    ranges = mapset.process(ranges)
    # wait_for_input()
    # logger.success(ranges)

min_location = min(ranges, key=lambda rng: rng.start)
print(min_location)
