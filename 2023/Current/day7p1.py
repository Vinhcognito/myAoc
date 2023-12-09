from __future__ import annotations

import copy
from collections import Counter
from dataclasses import dataclass, field
from functools import reduce
from itertools import count
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

DAY = 7

locations = get_locations(f"day{DAY}")
logger.add(f"{locations.log_file}", backtrace=True, diagnose=True)
logger_config(logger)
clear_terminal()

"""
33332 > 2AAAA 
77888 > 77788
types:
5oak 6
4oak 5
fh 4
3oak 3
2p 2
1p 1
high 0
"""

cardvals = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
cardvals_p2 = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]
content = read_input(locations.input_file)
cl = content.split("\n")


class Hand:
    def __init__(self, line):
        split = line.split(" ")
        self.cards = [c for c in split[0]]
        self.bid = int(split[1])
        self.counts = Counter(self.cards)
        self.type = 0

        self.get_type()

    def get_type(self):
        match len(self.counts.keys()):
            case 1:
                self.type = 6  # 5oak
            case 2:
                for val in self.counts.values():
                    if val == 4 or val == 1:
                        self.type = 5  # 4oak
                    else:
                        self.type = 4  # fh
            case 3:
                if max(self.counts.values()) == 3:
                    self.type = 3  # 3oak
                else:
                    self.type = 2  # 2p
            case 4:
                self.type = 1  # 1p
            case 5:
                self.type = 0  # high

    @staticmethod
    def compare_cards(card1, card2):
        if card1 == card2:
            return -1
        else:
            if cardvals.index(card1) > cardvals.index(card2):
                return 1
            else:
                return 0

    def is_outrank(self, otherhand: Hand):
        """if this > otherhand, return true"""
        if self.type > otherhand.type:
            return True
        elif self.type < otherhand.type:
            return False
        else:
            for i in range(5):
                match Hand.compare_cards(self.cards[i], otherhand.cards[i]):
                    case -1:
                        continue
                    case 1:
                        return True
                    case 0:
                        return False
        return True

    def __str__(self):
        return "".join(self.cards)

    def __gt__(self, other):
        return self.is_outrank(other)

    def __lt__(self, other):
        return not self.is_outrank(other)


hands = []
for line in cl:
    hands.append(Hand(line))

hands.sort()

sum = 0
for rank, hand in enumerate(hands, 1):
    sum += hand.bid * rank

print(f"Part 1 sum : {sum}")
