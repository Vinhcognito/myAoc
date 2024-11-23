import re
from collections import Counter
from dataclasses import dataclass, field
from functools import cache, reduce
from itertools import combinations, combinations_with_replacement, permutations
from pprint import pprint

from decorators import timer
from helpers import Point, get_locations, read_input
from loguru import logger
from util import (
    clear_terminal,
    extend_list,
    extend_list_2D,
    extend_list_rect,
    logger_config,
    print_array,
    wait_for_input,
)

DAY = 12

locations = get_locations(f"day{DAY}")
# logger.add(f"{locations.log_file}", backtrace=True, diagnose=True)
logger_config(logger)
clear_terminal()

content = read_input(locations.example_file)
lines = content.split("\n")


def replace_unknowns(input: str, replacement: str) -> str:
    replace_i = 0
    for i, char in enumerate(input):
        if char == "?":
            input = input[:i] + replacement[replace_i] + input[i + 1 :]
            replace_i += 1
    return input


"""too slow
def get_unique_perms(input):
    sorted_list = sorted(list(input))
    perms = set(permutations(sorted_list))
    # Convert the permutations back to strings
    perms = ["".join(p) for p in perms]
    return perms


def check_validity(row: str, valid_groups: list[int]) -> bool:
    groups = row.split(".")
    groups = [len(s) for s in filter(lambda x: x != "", groups)]
    if groups == valid_groups:
        # logger.debug(f"row:{row}")
        # logger.debug(f"groups:{groups}")
        # logger.debug(f"valid:{valid_groups}")
        return True
    else:
        # logger.warning(f"row:{row}")
        # logger.warning(f"groups:{groups}")
        # logger.warning(f"valid:{valid_groups}")
        return False



def count_valid(comb: str, groups: list[int]) -> int:
    count = 0
    for perm in get_unique_perms(comb):
        # logger.debug(perm)
        if check_validity(replace_unknowns(row, perm), groups):
            count += 1
    print(f"count was:{count}")
    return count
    
count = 0
i = 0
for line in lines:
    i += 1
    print(f"line {i}")
    groups = [int(s) for s in line.split(" ")[1].split(",")]
    row = line.split(" ")[0]
    # determine number of #
    hash_count = sum(groups) - row.count("#")
    comb = "" + "#" * hash_count + "." * (row.count("?") - hash_count)
    count += count_valid(comb, groups)
print(count)
"""
