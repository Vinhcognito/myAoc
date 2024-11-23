import re
from collections import Counter
from dataclasses import dataclass, field
from functools import reduce
from pprint import pprint

from decorators import timer
from helpers import Point, Vectors, get_locations, read_input
from loguru import logger
from util import (
    clear_terminal,
    extend_list,
    extend_list_2D,
    extend_list_rect,
    logger_config,
    print_array,
    wait_for_input,
)

DAY = 19

locations = get_locations(f"day{DAY}")
# logger.add(f"{locations.log_file}", backtrace=True, diagnose=True)
logger_config(logger)
clear_terminal()


class Part:
    def __init__(
        self,
        workflow: str,
        x: tuple[int, int],
        m: tuple[int, int],
        a: tuple[int, int],
        s: tuple[int, int],
    ):
        self.x = x
        self.m = m
        self.a = a
        self.s = s
        self.workflow = workflows[workflow]
        self.accepted: bool | None = None

    def process(self):
        rules = self.workflow.get_rules()
        splits = []
        for rule in rules:
            # determine how the rule splits this parts intervals
            # create new part for each split and add to stack
            

    def split(self):

    def __str__(self):
        return f"x:{self.x},m:{self.m},a:{self.a},s:{self.s}"


class Rule:
    delimiters = ["<", ">"]

    def __init__(self, input: str):
        self.auto = False

        if input.find(":") != -1:
            if input.find("<") != -1:
                self.compare = "<"
            else:
                self.compare = ">"
            self.condstr, self.dest = input.split(":")
            self.cat, self.val = re.split(
                "|".join(map(re.escape, Rule.delimiters)), self.condstr
            )
        else:
            self.auto = True
            self.dest = input

    def test(self, part: Part) -> bool:
        if self.auto:
            return True
        else:
            part_value = getattr(part, self.cat)
            return eval(f"{part_value}{self.compare}{self.val}")

    def __str__(self):
        if self.auto:
            return f"Auto -> {self.dest}"
        else:
            return f"{self.cat} {self.compare} {self.val} -> {self.dest}, "


class Workflow:
    def __init__(self, line: str):
        self.name, self.rulestr = line.split("{")
        self.rules = [Rule(str) for str in self.rulestr[:-1].split(",")]

    def get_rules(self):
        return self.rules

    def __str__(self):
        output = [self.name, " has ruleset:"]
        for rule in self.rules:
            output.append("  ")
            output.append(str(rule))
        return "".join(output)


content = read_input(locations.example_file)

workflows: dict[str, Workflow] = {}

for line in content.split("\n\n")[0].split("\n"):
    name = line.split("{")[0]
    workflows[name] = Workflow(line)

init_range = (1, 4001)
starting_part = Part("in", init_range, init_range, init_range, init_range)
