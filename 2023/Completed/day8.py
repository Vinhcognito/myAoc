import re
from math import gcd, lcm

from helpers import get_locations, read_input

DAY = 8

locations = get_locations(f"day{DAY}")

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
