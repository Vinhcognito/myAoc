import re
from dataclasses import dataclass

from helpers import Point, get_locations, read_input  # noqa: F401
from util import (  # noqa: F401
    ints,
)

DAY = 3
locations = get_locations(f"day{DAY}")
content = read_input(locations.input_file)
cl = content.split("\n")


@dataclass
class Part:
    point: Point
    length: int
    value: int

    def get_adjacent(self):
        li = []
        for i in range(self.length):
            li.extend(Point(self.point.x, self.point.y + i).neighbours())
        return li


### part 1
symbol_dict = {}
parts = []

for i, line in enumerate(cl):
    # get symbols
    matches = re.finditer(r"[^0-9.]", line)
    for s in matches:
        pos = Point(i, s.start())
        symbol_dict[pos] = s.group()

    # get parts
    int_list, pos_list = ints(line, signs=False)

    for j, p in enumerate(int_list):
        parts.append(
            Part(
                Point(i, pos_list[j]),
                len(str(p)),
                int(p),
            )
        )

valid = []

# look for valid part numbers
for part in parts:
    for pos in part.get_adjacent():
        if pos in symbol_dict:
            valid.append(part)
            break

sum = 0
for part in valid:
    sum += part.value

print(f"part 1 sum = {sum}")

#### part 2


symbol_dict = {}
parts = []

for i, line in enumerate(cl):
    # get gear symbols
    matches = re.finditer(r"[^0-9.]", line)
    for s in matches:
        if s.group() == "*":
            pos = Point(i, s.start())
            symbol_dict[pos] = []

    # get parts
    int_list, pos_list = ints(line, signs=False)

    for j, p in enumerate(int_list):
        parts.append(
            Part(
                Point(i, pos_list[j]),
                len(str(p)),
                int(p),
            )
        )

valid = []

# count part#s by all the gears
for part in parts:
    for pos in part.get_adjacent():
        if pos in symbol_dict:
            symbol_dict[pos].append(part)
            break

sum = 0
# look for valid gears
for gear, part_arr in symbol_dict.items():
    if len(part_arr) == 2:
        sum += part_arr[0].value * part_arr[1].value

print(f"Part 2 sum of gear ratios: {sum}")
