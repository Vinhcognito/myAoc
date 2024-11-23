import re
from collections import Counter
from dataclasses import dataclass, field
from functools import reduce
from pprint import pprint

from helpers import Point, get_locations, read_input
from loguru import logger
from util import (
    clear_terminal,
    extend_list,
    extend_list_2D,
    extend_list_rect,
    logger_config,
    print_array,
)

DAY = 99

locations = get_locations(f"day{DAY}")
# logger.add(f"{locations.log_file}", backtrace=True, diagnose=True)
logger_config(logger)
clear_terminal()

content = read_input(locations.input_file)
rows = content.split("\n").reverse()


grid = []
for y, row in enumerate(rows):
    print(row)
    grid.append([])
    for x, c in enumerate(row):
        grid[x].append(int(c))

pprint(grid)


def dfs(array, x, y, visited):
    # Define the directions for the neighbors
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # If the location is within the array and has not been visited yet
    if (0 <= x < len(array)) and (0 <= y < len(array[0])) and (not visited[x][y]):
        # Mark the location as visited
        visited[x][y] = True

        # Visit all the neighbors of the location
        for direction in directions:
            dfs(array, x + direction[0], y + direction[1], visited)


def connected_component_labeling(array):
    # Define the visited array
    visited = [[False for _ in range(len(array[0]))] for _ in range(len(array))]

    # Define the label counter
    label = 1

    # Define the labels for each location
    labels = [[0 for _ in range(len(array[0]))] for _ in range(len(array))]

    # Scan the array from top to bottom and left to right
    for x in range(len(array)):
        for y in range(len(array[0])):
            # If the location is not visited yet
            if not visited[x][y]:
                # Label the location and its neighbors with the new label
                dfs(array, x, y, visited)

                # Increment the label counter
                label += 1

    return labels
