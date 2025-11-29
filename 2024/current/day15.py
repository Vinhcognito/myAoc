from __future__ import annotations

import enum
import math
import re
from collections import Counter, defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from functools import reduce
from itertools import combinations
from pprint import pprint
from typing import Any, ItemsView, Type

from shared.decorators import timer
from shared.helpers import Point, Vectors, get_locations, read_input
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

DAY = 15

logger_init()
logger_enable(log, f"day{DAY}")

locations = get_locations(f"day{DAY}")

N = Point(0, -1)
E = Point(1, 0)
S = Point(0, 1)
W = Point(-1, 0)
dirs = [N, E, S, W]


def get_neighbours(point: Point) -> list[Point]:
    return [point + vec for vec in dirs]


class Grid:
    def __init__(self, input: str):
        self.g: dict[Point:str] = {}
        self.g2: dict[Point:str] = {}
        self.input = input
        self.valid: set[Point] = set()
        self.robot: Point
        self.r2: Point

        self.g_str, self.movements = input.split("\n\n")
        self.g_str = self.g_str.split("\n")

        self.rows = len(self.g_str)
        self.cols = len(self.g_str[0])

        self.rows2 = self.rows
        self.cols2 = self.cols * 2

        for y, line in enumerate(self.g_str):
            p = Point(0, y)
            for x, v in enumerate(line):
                match v:
                    case "#" | ".":
                        self.g2[p] = v
                        p += E
                        self.g2[p] = v
                    case "O":
                        self.g2[p] = "["
                        p += E
                        self.g2[p] = "]"
                    case "@":
                        self.g2[p] = "."
                        self.r2 = p
                        p += E
                        self.g2[p] = "."
                p += E

                self.g[Point(x, y)] = v
                if v == "@":
                    self.robot = Point(x, y)
                    self.g[self.robot] = "."

    def print_grid2(self):
        p_grid = deepcopy(self.g2)
        p_grid[self.r2] = "@"

        for y in range(self.rows2):
            print("".join([p_grid[Point(x, y)] for x in range(self.cols2)]))

    def part_two(self):
        self.print_grid2()
        for step in self.movements:
            self.step2(step)
            # print(step)
        score = 0

        for p, c in self.g2.items():
            if c == "[":
                score += self.get_box_score2(p)

        self.print_grid2()
        return score

    def step2(self, dir: str):
        vector: Point
        match dir:
            case "<":
                vector = W
            case ">":
                vector = E
            case "^":
                vector = N
            case "v":
                vector = S
            case _:
                return

        if self.check_step(vector):
            self.r2 += vector
        else:
            if not self.is_wall(vector):
                self.push_box2(vector)

    def push_box2(self, dir: Point):
        self.valid = set()
        # find other half of box
        # box = left, right
        half_box = self.r2 + dir
        if self.g2[half_box] == "[":
            other_half = half_box + E
        else:
            other_half = half_box + W

        # check both points the box moves into:
        #### repeat check for each box found
        #### if any is blocked, no movement

        if self.is_box_blocked(half_box, dir) or self.is_box_blocked(other_half, dir):
            return
        else:
            print(f"Moving {dir}")
            self.print_grid2()
            print()
            move_dict = {}

            for p in self.valid:
                move_dict[p] = deepcopy(self.g2[p])
                self.g2[p] = "."

            for p, v in move_dict.items():
                self.g2[p + dir] = v

            self.g2[self.r2] = "."
            self.r2 += dir

            self.print_grid2()
            print()

    def is_box_blocked(self, p: Point, dir: Point, done=False) -> bool:
        """checks if box at p can move in dir"""
        if p == Point(16, 4) and dir == Point(0, -1):
            print()
        new_p = p + dir

        match self.g2[new_p]:
            case "#":
                return True
            case ".":
                self.valid.add(p)
                p_other_half: Point
                if self.g2[p] == "[":
                    p_other_half = p + E
                else:
                    p_other_half = p + W
                return False
            case "[" | "]":
                self.valid.add(p)
                p_other_half: Point
                if self.g2[p] == "[":
                    p_other_half = p + E
                else:
                    p_other_half = p + W
                self.valid.add(p_other_half)

                if not self.is_box_blocked(new_p, dir):
                    other_half: Point
                    if self.g2[new_p] == "[":
                        other_half = new_p + E
                    else:
                        other_half = new_p + W
                    self.valid.add(other_half)
                    if not done:
                        return self.is_box_blocked(other_half, dir, True)
                else:
                    return True

    def get_box_score2(self, p: Point):
        return 100 * p.y + p.x

    def check_step(self, dir_vector: Point):
        return self.g2[self.r2 + dir_vector] == "."

    def is_wall(self, dir_vector: Point):
        return self.g2[self.r2 + dir_vector] == "#"

    """
    def print_grid(self):
        p_grid = deepcopy(self.g)
        p_grid[self.robot] = "@"

        for y in range(self.rows):
            print("".join([p_grid[Point(x, y)] for x in range(self.cols)]))
            
    def part_one(self):
        self.print_grid()
        for step in self.movements:
            self.step(step)
        score = 0
        for p, c in self.g.items():
            if c == "O":
                score += self.get_box_score(p)

        return score

    def get_box_score(self, p: Point):
        return 100 * p.y + p.x

    def step(self, dir: str):
        vector: Point
        match dir:
            case "<":
                vector = W
            case ">":
                vector = E
            case "^":
                vector = N
            case "v":
                vector = S
            case _:
                return

        if self.check_step(vector):
            self.robot += vector
        else:
            if not self.is_wall(vector):
                self.push_box(vector)

    def push_box(self, dir: Point):
        # find first empty space in the direction
        # move boxes between robot and empty space, 1 space in the direction
        pos = self.robot + dir
        while self.g[pos] != "." and self.g[pos] != "#":
            pos += dir

        if self.g[pos] == ".":
            self.shift(self.robot, pos, dir)

    def shift(self, start: Point, end: Point, dir: Point):
        print(f"start:{start}, robot:{self.robot} end:{end} dir:{dir}")
        self.g[start] = "."
        self.robot = start + dir
        self.g[self.robot] = "."
        self.g[end] = "O"

    

    
    """


example_content = read_input(locations.example_file)
example_cl = example_content.split("\n")
example_cl = example_cl[3:-4]

content = read_input(locations.input_file)
cl = content.split("\n")


@timer
def part1(input):
    g = Grid(input)

    # return f"{g.part_one()}"

    return "Not implemented"


@timer
def part2(input):
    g = Grid(input)

    return f"{g.part_two()}"


print("------------------------------------------------------------")
print("EXAMPLE INPUT")
print("------------------------------------------------------------")
example_input = example_content
print(part1(example_input))
print()
print(part2(example_input))

"""
print()
print()
print("------------------------------------------------------------")
print("REAL INPUT")
print("------------------------------------------------------------")
input = content
print(part1(input))
print()
print(part2(input))
"""
