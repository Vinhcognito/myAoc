from dataclasses import dataclass
from functools import cached_property


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point):
        return Point(self.x + other.x, self.y + other.y)

    @cached_property
    def get_neighbours_cached(self) -> list[Point]:
        li = []
        for d in dirs:
            p = self + d
            li.append(p)
        return li

    def get_neighbours(self) -> list[Point]:
        li = []
        for d in dirs:
            p = self + d
            li.append(p)
        return li


U = Point(0, -1)
UR = Point(1, -1)
R = Point(1, 0)
DR = Point(1, 1)
D = Point(0, 1)
DL = Point(-1, 1)
L = Point(-1, 0)
UL = Point(-1, -1)
dirs = [UL, U, UR, L, R, DL, D, DR]


def part_one(input: str):
    lines = input.strip().split("\n")
    grid: dict[Point, str] = {}

    def is_accessible(p: Point) -> bool:
        count = 0
        for n in p.get_neighbours():
            neighbour = grid.get(n)
            if neighbour is not None:
                count += 1
                if count >= 4:
                    break

        if count < 4:
            return True
        return False

    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            if c == "@":
                grid[Point(col, row)] = c

    count = 0
    for p in grid.keys():
        if grid[p] == "@" and is_accessible(p):
            count += 1
    return count


def part_two(input: str):
    lines = input.strip().split("\n")
    grid: dict[Point, str] = {}

    def is_accessible(p: Point) -> bool:
        count = 0
        for n in p.get_neighbours_cached:
            neighbour = grid.get(n)
            if neighbour is not None:
                count += 1
                if count >= 4:
                    break

        if count < 4:
            return True
        return False

    for row, line in enumerate(lines):
        for col, c in enumerate(line):
            if c == "@":
                grid[Point(col, row)] = c

    count = 0
    prev_count = count
    while True:
        prev_count = count
        for p in [p for p in grid.keys()]:
            if is_accessible(p):
                grid[p] = "."
                del grid[p]
                count += 1
        if count == prev_count:
            break
    return count
