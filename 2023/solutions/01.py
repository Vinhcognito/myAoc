import sys
import utils
from aocd.examples import Example
from aocd.models import Puzzle

# data: str = sys.stdin.read()


# data: str = Puzzle(2025, day=1).examples[0].input_data
data: str = Puzzle(2025, 1).input_data


def part_one(data: str):
    lines = data.split("\n")
    utils.cat()


def part_two(data: str):
    lines = data.split("\n")
    print("test2")


print(part_one(data))
print(part_two(data))
