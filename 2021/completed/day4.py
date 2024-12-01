from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from functools import reduce
from pprint import pprint

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
logger_enable(log, "day1")

DAY = 4

locations = get_locations(f"day{DAY}")


# content = read_input(locations.example_file)
content = read_input(locations.input_file)

cl = content.split("\n")

numbers = ints(cl[0])[0]


"""
Part 1
class Board:
    '''board:dict{value:(board row, board col)}'''

    def __init__(self, li: list):
        self.li = li
        self.board = {}
        self.marked = {}
        for i in range(5):
            for j in range(5):
                self.board[li[i * 5 + j]] = (i, j)

    def check(self, number: int) -> bool:
        '''number was called, mark it off and then check if won'''
        pos = self.board.get(number, False)
        if pos is not False:
            del self.board[number]
            self.marked[pos] = 1
            if self.win_check(pos):
                self.calc_win(number)
                return True
        return False

    def win_check(self, pos: tuple[int, int]):
        # check row
        count = 0
        for col in range(5):
            if self.marked.get((pos[0], col), 0) == 1:
                count += 1
            else:
                break

        if count == 5:
            print(f"This board:{self.li} has won")
            return True
        else:
            count = 0

        # check column
        for row in range(5):
            if self.marked.get((row, pos[1]), 0) == 1:
                count += 1
            else:
                return False

        print(f"This board:{self.li} has won")
        return True

    def calc_win(self, number: int):
        sum = 0
        for key in self.board.keys():
            sum += key
        print(f"sum of unamarked numbers = :{sum}")
        print(f"PART 1: WINNING score = sum * number: {number} = {sum*number}")
        exit()

    def __str__(self):
        result = "".join(map(str, li))
        return result


boards: list[Board] = []
li = []
for i, line in enumerate(cl[2:]):
    li.extend(ints(line)[0])
    if len(li) == 25:
        b = Board(li)
        boards.append(b)
        li = []


for number in numbers:
    for b in boards:
        b.check(number)
"""


# PART 2
class Board:
    """board:dict{(row,col):value}"""

    def __init__(self, li: list):
        self.li = li
        self.board = {}
        self.unmarked_sum = sum(li)
        for i in range(5):
            for j in range(5):
                self.board[(i, j)] = li[i * 5 + j]

    def check(self, number: int) -> bool:
        """number was called, mark it off and then check if won"""
        if number in self.li:
            row, col = self.get_pos(number)
            self.board[row, col] = 0
            self.unmarked_sum -= number
            if self.check_col(col) or self.check_row(row):
                self.calc_win(number)
                return True
        return False

    def get_pos(self, number) -> tuple[int, int]:
        index = self.li.index(number)
        row = index // 5
        col = index % 5
        return row, col

    def check_row(self, row: int):
        # check row for a win
        sum = 0
        for col in range(5):
            sum += self.board[row, col]

        if sum == 0:
            return True
        return False

    def check_col(self, col: int):
        # check col for a win
        sum = 0
        for row in range(5):
            sum += self.board[row, col]

        if sum == 0:
            return True
        return False

    def calc_win(self, number: int):
        print(f"sum of unamarked numbers = :{self.unmarked_sum}")
        print(f"WINNING score = sum * number: {number} = {number*self.unmarked_sum}")
        # exit()

    def __str__(self):
        result = "".join(map(str, li))
        return result


boards: list[Board] = []
li = []
for i, line in enumerate(cl[2:]):
    li.extend(ints(line)[0])
    if len(li) == 25:
        b = Board(li)
        boards.append(b)
        li = []

print(f"# of boards: {len(boards)}")
won = set()
for number in numbers:
    for i, b in enumerate(boards):
        if b.check(number):
            won.add(i)
        if len(won) == len(boards):
            exit()
