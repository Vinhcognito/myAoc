import re

from helpers import get_locations, read_input

DAY = 19

locations = get_locations(f"day{DAY}")
content = read_input(locations.example_file)


class Part:
    def __init__(self, x: int, m: int, a: int, s: int):
        self.x = x
        self.m = m
        self.a = a
        self.s = s
        self.accepted: bool | None = None

    @property
    def value(self) -> int:
        if self.accepted:
            return self.x + self.m + self.a + self.s
        else:
            return 0

    def process(self):
        current = "in"
        while self.accepted is None:
            next = workflows[current].consider(self)
            match next:
                case "A":
                    self.accepted = True
                    return self.value
                case "R":
                    self.accepted = False
                    return 0
                case _:
                    current = next
                    continue
        return 0

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

    def consider(self, part: Part) -> str:
        """returns the destination result of considering a part through this workflow"""
        for rule in self.rules:
            if rule.test(part):
                return rule.dest
            else:
                continue

    def __str__(self):
        output = [self.name, " has ruleset:"]
        for rule in self.rules:
            output.append("  ")
            output.append(str(rule))
        return "".join(output)


partstr = content.split("\n\n")[1].split("\n")

parts: list[Part] = []
workflows: dict[str, Workflow] = {}

for part in partstr:
    x, m, a, s = part[1:-1].split(",")
    parts.append(Part(int(x[2:]), int(m[2:]), int(a[2:]), int(s[2:])))

for line in content.split("\n\n")[0].split("\n"):
    name = line.split("{")[0]
    workflows[name] = Workflow(line)

p1_sum = 0
for part in parts:
    p1_sum += part.process()

print(f"Part 1: Sum of accepted parts' values is {p1_sum}")
