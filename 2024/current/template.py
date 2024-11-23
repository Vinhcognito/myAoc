import math
import re
from collections import Counter
from dataclasses import dataclass, field
from functools import reduce
from pprint import pprint

from shared.helpers import Grid, Point, Vectors, get_locations, read_input
from shared.util import (
    extend_list,
    extend_list_2D,
    extend_list_rect,
    log,
    logger_config,
    logger_enable,
    logger_init,
    print_array,
    wait_for_input,
)

logger_init()
logger_enable(log, "day1")

DAY = 8

locations = get_locations(f"day{DAY}")


content = read_input(locations.example_file)
content = read_input(locations.input_file)
cl = content.split("\n")
