import math
import re
from collections import Counter
from dataclasses import dataclass, field
from functools import reduce
from pprint import pprint

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

logger_init()
logger_enable(log, "4")

DAY = 4

locations = get_locations(f"day{DAY}")


# content = read_input(locations.example_file)
content = read_input(locations.input_file)

cl = content.split("\n")


class Grid:
    def __init__(self, input_li: list[str]):
        self.grid = {}
        self.li = input_li
        self.rows = len(input_li)
        self.cols = len(input_li[0])
        self.matches = 0
        self.rowmatches = 0
        self.colmatches = 0
        self.drmatches = 0
        self.dlmatches = 0
        self.mases = 0
        self.init_grid()

    @timer
    def part_one(self):
        self.rowmatches = self.check_rows()
        self.colmatches = self.check_cols()
        self.check_diags()
        print(f"row matches:{self.rowmatches}")
        print(f"col matches:{self.colmatches}")
        print(f"dr matches:{self.drmatches}")
        print(f"dl matches:{self.dlmatches}")

    def init_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.grid[Point(row, col)] = self.li[row][col]

    def check_rows(self):
        sum = 0
        for row in self.li:
            sum += self.find_all_xmas(row)
        return sum

    def get_col(self, col) -> str:
        result_li = [value for key, value in self.grid.items() if key.y == col]
        return "".join(result_li)

    def check_cols(self):
        sum = 0
        for col in range(self.cols):
            colstr = self.get_col(col)
            sum += self.find_all_xmas(colstr)
        return sum

    def get_diag_DR(self, origin: Point):
        p = origin
        diagstr = ""
        while self.grid.get(p, 0) != 0:
            diagstr += self.grid[p]
            p += Point(1, 1)
        return "".join(diagstr)

    def get_diag_DL(self, origin: Point):
        p = origin
        diagstr = ""
        while self.grid.get(p, 0) != 0:
            diagstr += self.grid[p]
            p += Point(1, -1)
        return "".join(diagstr)

    def check_diags(self):
        dr = 0
        dl = 0
        # check diags going down+right
        for row in range(1, self.rows):
            dr += self.find_all_xmas(self.get_diag_DR(Point(row, 0)))
        # print(f"row dr matches:{self.matches}")
        for col in range(self.cols):
            dr += self.find_all_xmas(self.get_diag_DR(Point(0, col)))
        self.drmatches += dr
        # print(f"col dr matches:{self.matches}")

        # check diags going down+left

        for row in range(1, self.rows):
            dl += self.find_all_xmas(self.get_diag_DL(Point(row, self.cols - 1)))
        # print(f"row dl matches:{self.matches}")
        for col in range(self.cols):
            dl += self.find_all_xmas(self.get_diag_DL(Point(0, col)))
        # print(f"col dl matches:{self.matches}")
        self.dlmatches += dl

    def find_all_xmas(self, string):
        """finds all matches for XMAS and SAMX"""
        result1 = [m.start() for m in re.finditer("XMAS", string)]
        result2 = [m.start() for m in re.finditer("SAMX", string)]

        self.matches += len(result1)
        self.matches += len(result2)

        return len(result1) + len(result2)

    # Part 2
    @timer
    def part_two(self):
        """get every 3x3 box in the grid and check for mas"""
        for row in range(self.rows - 2):
            for col in range(self.cols - 2):
                if self.check_mas(self.get_box_str(Point(row, col))):
                    # log.info(f"\nmas in {Point(row,col)}")
                    self.mases += 1
                else:
                    pass
                    # log.error(f"\nNO mas in {Point(row,col)}")

    def check_mas(self, li: list[str]):
        """checks if 3x3 box has a match"""
        if li[4] == "A":
            substr: str = "".join(li[0] + li[2] + li[6] + li[8])
            if substr.count("M") == 2 and substr.count("S") == 2:
                # check for MAM and SAS
                if substr != "MSSM" and substr != "SMMS":
                    return True
        return False

    def get_box_str(self, p: Point) -> list[str]:
        """gets a 3x3 array arranged into a 1d list, based on the top left Point"""
        r1 = [
            self.grid[p], 
            self.grid[p + Point(0, 1)], 
            self.grid[p + Point(0, 2)]
        ]  # fmt: skip
        r2 = [
            self.grid[p + Point(1, 0)],
            self.grid[p + Point(1, 1)],
            self.grid[p + Point(1, 2)],
        ]
        r3 = [
            self.grid[p + Point(2, 0)],
            self.grid[p + Point(2, 1)],
            self.grid[p + Point(2, 2)],
        ]
        # log.debug(f"\n{''.join(r1)}\n{''.join(r2)}\n{''.join(r3)}")
        r1.extend(r2)
        r1.extend(r3)
        return r1


grid = Grid(cl)

grid.part_one()
print(f"Part one: {grid.matches}")

grid.part_two()
print(f"Part two: {grid.mases}")
