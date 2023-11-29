from helpers import get_locations, read_input
from loguru import logger  # noqa
from util import wipeTerminal

DAY = 1

locations = get_locations(f"day{DAY}")
# logger.add(f"{locations.log_file}", backtrace=True, diagnose=True)
wipeTerminal()

content = read_input(locations.input_file)
cl = content.split("\n")

for line in cl:
    print(line)

# printArray(cl, [0, 0])
