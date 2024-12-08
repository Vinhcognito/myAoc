from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from functools import reduce
from pprint import pprint

from shared.decorators import timer
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
logger_enable(log, "5")

DAY = 5

locations = get_locations(f"day{DAY}")


# content = read_input(locations.example_file)
content = read_input(locations.input_file)
cl = content.split("\n")


class Rules:
    d: defaultdict[int : list[int]]
    rule_input: list[str]

    def __init__(self, rule_inputs: list[str]):
        self.d = defaultdict(list)
        for rule_str in rule_inputs:
            before, after = rule_str.split("|")
            self.d[int(before)].append(int(after))

    def check_lt(self, a: int, b: int) -> bool:
        if b in self.d[a]:
            return True
        elif a in self.d[b]:
            return False
        else:
            return False


rules = Rules(cl[: cl.index("")])
update_str = cl[cl.index("") + 1 :]


class Update:
    def __init__(self, update_str: list[str]):
        self.update_str = update_str
        self.li = ints(update_str)[0]

        self.pages = []
        for p in self.li:
            self.pages.append(Page(p))

    def is_valid(self):
        self.pages.sort()
        lis = []
        for p in self.pages:
            lis.append(p.v)

        return self.li == lis

    def get_mid(self) -> int:
        mid = math.floor(len(self.pages) / 2)
        print(f"mid={mid}")
        return self.pages[mid].v


@dataclass
class Page:
    v: int

    def __lt__(self, other: Page):
        return rules.check_lt(self.v, other.v)

    def __gt__(self, other: Page):
        return rules.check_lt(other.v, self.v)


updates = []
for line in update_str:
    updates.append(Update(line))


sum_p1 = 0
sum_p2 = 0
for update in updates:
    if update.is_valid():
        sum_p1 += update.get_mid()
    else:
        sum_p2 += update.get_mid()

print(f"part1:{sum_p1}")
print(f"part2:{sum_p2}")
