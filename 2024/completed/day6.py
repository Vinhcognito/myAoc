import math
import re
from collections import Counter
from dataclasses import dataclass, field
from functools import reduce
from pprint import pprint

from shared.decorators import timer
from shared.helpers import Point, Vectors, get_locations, read_input
from shared.util import (
    clamp,
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
logger_enable(log, "6")

DAY = 6

locations = get_locations(f"day{DAY}")


content = read_input(locations.example_file)
# content = read_input(locations.input_file)


class Guard:
    # NESW, r x c
    directions = [
        Point(-1,0),
        Point(0,1),
        Point(1,0),
        Point(0,-1),
    ]  # fmt: skip

    def __init__(self, p: Point, dir: Point):
        self.p: Point = p
        # init dir
        self.dir_index = self.directions.index(dir)

        self.visited: Counter[Point] = Counter()
        self.visited[self.p] += 1

        self.looped = False

    @property
    def dir(self) -> Point:
        """return vector of current facing"""
        return self.directions[self.dir_index % 4]

    def forward(self):
        self.p += self.dir
        self.visited[self.p] += 1
        if self.visited[self.p] >= 5:
            self.looped = True

    def turn_right(self):
        self.dir_index += 1

    def get_total_visited(self) -> int:
        return sum(value > 0 for value in self.visited.values())

    def get_all_visited(self):
        return [key for key, value in self.visited.items() if value > 0]


class Grid:
    def __init__(self, input: str, obstacle: Point = None):
        self.input = input
        self.d: dict[Point:str] = {}
        self.guard: Guard
        self.rows: int
        self.cols: int

        cl = input.split("\n")

        self.rows = len(cl)
        self.cols = len(cl[0])

        for row, line in enumerate(cl):
            for col, c in enumerate(line):
                match c:
                    case "#" | ".":
                        self.d[Point(row, col)] = c
                    case "^":
                        self.guard = Guard(Point(row, col), Point(-1, 0))

        # for part 2
        if obstacle is not None:
            self.d[obstacle] = "#"

    def step(self) -> bool:
        """true if empty, false if blocked"""
        if self.d.get(self.guard.p + self.guard.dir, 0) == "#":
            # log.debug(f"guard turn, # @ {self.guard.p + self.guard.dir}")
            self.guard.turn_right()
        else:
            self.guard.forward()
            # log.debug(f"guard forward, now @ {self.guard.p}")

    def check_limits(self):
        if (
            self.guard.p.x == -1
            or self.guard.p.x == self.cols
            or self.guard.p.y == -1
            or self.guard.p.y == self.rows
        ):
            return False
        else:
            return True

    def get_total_steps_p1(self):
        return self.guard.get_total_visited() - 1


@timer
def part1():
    grid = Grid(content)
    while grid.check_limits():
        grid.step()

    print(f"Part1: {grid.get_total_steps_p1()}")


@timer
def part2():
    grid = Grid(content)
    while grid.check_limits():
        grid.step()

    looped_count = 0

    for obs in grid.guard.get_all_visited():
        grid = Grid(content, Point(obs.x, obs.y))
        # log.debug(f"checking obs @ {Point(obs.x,obs.y)}")
        while grid.check_limits():
            grid.step()
            if grid.guard.looped:
                looped_count += 1
                break

    print(f"Part2: {looped_count}")


part1()

part2()
