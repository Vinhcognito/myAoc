import re
from collections import Counter
from dataclasses import dataclass, field
from functools import reduce
from math import gcd, lcm
from pprint import pprint

from helpers import Grid, Point, get_locations, read_input
from loguru import logger
from util import (
    clear_terminal,
    extend_list,
    extend_list_2D,
    extend_list_rect,
    logger_config,
    print_array,
)

DAY = 8

locations = get_locations(f"day{DAY}")
logger.add(f"{locations.log_file}", backtrace=True, diagnose=True)
logger_config(logger)
clear_terminal()

content = read_input(locations.input_file)
cl = content.split("\n")

instructions = [char for char in cl[0]]

maps = {}
for line in cl[2:]:
    result = re.findall(r"\b\w{3}\b", line)
    maps[result[0]] = (result[1], result[2])


# for part 1
def walk(node):
    step = 0
    while True:
        if instructions[step % len(instructions)] == "L":
            node = maps[node][0]
        else:
            node = maps[node][1]
        step += 1
        if node == "ZZZ":
            return step


print(f"Steps for part 1: {walk("AAA")}")


def find_z_cycle(node):
    li = []
    step = 0
    while True:
        if instructions[step % len(instructions)] == "L":
            node = maps[node][0]
        else:
            node = maps[node][1]
        step += 1
        if node[2] == "Z":
            li.append(step)
        if len(li) > 3:
            if li[-1] - li[-2] == li[-2] - li[-3]:
                return li[-2] - li[-3]


start_nodes = list(
    filter(
        lambda node: node[2] == "A",  # noqa
        [node for node in maps.keys()],
    )
)

z_cycles = []
for node in start_nodes:
    z_cycles.append(find_z_cycle(node))

common = 1
for z in z_cycles:
    common = lcm(common, z)

print(f"steps for part 2: {common}")
