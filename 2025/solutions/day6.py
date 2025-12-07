from collections import defaultdict
from math import prod


def part_one(input: str):
    from shared.util import ints

    lines = input.strip().split("\n")
    rows = len(lines) - 1

    d = {}
    for row, line in enumerate(lines[:-1]):
        values = ints(line)[0]

        for col, value in enumerate(values):
            d[row, col] = value

    sum = 0
    for i, sign in enumerate(lines[-1].replace(" ", "")):
        if sign == "+":
            result = 0
            for row in range(rows):
                result += d[row, i]
        else:
            result = 1
            for row in range(rows):
                result *= d[row, i]

        sum += result
    return sum


class Problem:
    def __init__(self, input: list[str]):
        self.sign = input[-1].replace(" ", "")
        self.ints = []
        rows = len(input)
        # process input
        for col in range(len(input[0])):
            result = ""
            for row in range(rows - 1):
                if input[row][col] != " ":
                    result += input[row][col]
            if result != "":
                self.ints.append(int(result))

    def solve(self):
        if self.sign == "*":
            return prod(self.ints)
        else:
            return sum(self.ints)

    def __str__(self):
        return f"{self.sign} " + f"{self.ints}"


def part_two(input: str):
    lines = input.split("\n")
    rows = len(lines)
    sign_indexes = [i for i, c in enumerate(lines[-1]) if c == "*" or c == "+"]

    d = defaultdict(list)

    for i in range(rows):
        for col in range(len(sign_indexes)):
            if col != len(sign_indexes) - 1:
                d[col].append(lines[i][sign_indexes[col] : sign_indexes[col + 1]])
            else:
                d[col].append(lines[i][sign_indexes[col] :])

    sum = 0
    for col in d.keys():
        p = Problem(d[col])
        sum += p.solve()

    return sum
