from helpers import get_locations, read_input
from loguru import logger  # noqa
from util import clear_terminal

DAY = 14

locations = get_locations(f"day{DAY}")
# logger.add(f"{locations.log_file}", backtrace=True, diagnose=True)
clear_terminal()

content = read_input(locations.input_file)
cl = content.split("\n")

for line in cl:
    print(line)

# print_array(cl, [0, 0])
