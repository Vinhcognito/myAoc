import re

from shared.helpers import get_locations, read_input
from shared.util import log, logger_config, logger_enable, logger_init, text2int

DAY = 1

locations = get_locations(f"day{DAY}")

content = read_input(locations.input_file)
cl = content.split("\n")

NUMS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

# part 1
sum = 0

for line in cl:
    li = []
    sumstr = ""
    for c in line:
        if c in NUMS:
            li.append(c)

    sumstr = li[0] + li[-1]
    sum += int(sumstr)

logger_init()
logger_enable(log, "day1")

print(f"part 1 sum = {sum}")

# part 2
sum = 0

for line in cl:
    dict = {}
    sumstr = ""
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

print(f"part 2 sum = {sum}")
