import itertools  # noqa: F401
import re

from helpers import get_locations, read_input
from loguru import logger  # noqa: F401
from util import clear_terminal, text2int

DAY = 1

locations = get_locations(f"day{DAY}")
# logger.add(f"{locations.log_file}", backtrace=True, diagnose=True)
clear_terminal()

content = read_input(locations.input_file)
cl = content.split("\n")

NUMS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


# part 1
sum = 0
sumstr = ""

for line in cl:
    li = []
    for c in line:
        if c in NUMS:
            li.append(c)

    sumstr = li[0] + li[-1]
    sum += int(sumstr)
    sumstr = ""

logger.info(f"part 1 sum = {sum}")


# part 2
sum = 0
sumstr = ""

for line in cl:
    dict = {}
    for n, c in enumerate(line):
        if c in NUMS:
            dict[n] = c
    for word in WORDS:
        results = re.finditer(word, line)
        for ma in results:
            dict[ma.span()[0]] = text2int(word)

    k = list(dict.keys())

    k.sort()
    sumstr = str(dict[k[0]]) + str(dict[k[-1]])

    sum += int(sumstr)
    sumstr = ""
logger.info(f"part 2 sum = {sum}")
