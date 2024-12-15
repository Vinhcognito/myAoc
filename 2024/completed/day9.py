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
logger_enable(log, "9")

DAY = 9

locations = get_locations(f"day{DAY}")


# content = read_input(locations.example_file)
content = read_input(locations.input_file)


class DiskMap:
    def __init__(self, input):
        self.files = [int(val) for val in input[::2]]
        self.spaces = [int(val) for val in input[1::2]]
        self.file_pos: list[int] = []

        self.disk: list[int] = []

        # gen initial disk state
        for id, size in enumerate(self.files):
            for i in range(size):
                self.disk.append(id)

            self.file_pos.append(len(self.disk) - 1)
            try:
                for i in range(self.spaces[id]):
                    self.disk.append(-1)
            except IndexError:
                break

    @timer
    def compact_part_one(self):
        right = len(self.disk) - 1

        for left in range(len(self.disk)):
            if left >= right:
                break
            if self.disk[left] != -1:
                continue
            else:
                self.disk[left] = self.disk[right]
                self.disk[right] = -1

                scan_end = True
                while scan_end:
                    right -= 1
                    if self.disk[right] != -1:
                        scan_end = False

        print("Part 1: ")
        self.checksum()

    @timer
    def compact_part_two(self):
        for id, size in enumerate(self.files[::-1]):
            # print(diskmap)
            file_id = len(self.files) - 1 - id

            gap = 0
            # check all the gaps
            for idx, val in enumerate(self.disk[: self.file_pos[file_id]]):
                if val == -1:
                    gap += 1
                # if gap of sufficient size is found
                if gap == size:
                    # move whole file to the gap
                    for i in range(size):
                        self.disk[self.disk.index(file_id)] = -1
                    for i in range(gap):
                        self.disk[idx - i] = file_id
                    break
                if val != -1:
                    gap = 0

        print("Part two: ")
        self.checksum()

    def get_key_by_value(self, dictionary, value):
        return [key for key, val in dictionary.items() if val == value]

    def print_dict(self, dict: dict):
        result = ""
        for value in dict.values():
            if value == -1:
                result += "."
            else:
                result += str(value)
        print(result)

    def checksum(self):
        sum = 0
        for idx, id in enumerate(self.disk):
            if id != -1:
                sum += idx * id

        print(f"Checksum = {sum}")

    def __str__(self):
        output = ""
        for n in self.disk:
            if n != -1:
                output += str(n)
            else:
                output += "."
        return "".join(output)


diskmap = DiskMap(content)
diskmap.compact_part_one()
diskmap.compact_part_two()
