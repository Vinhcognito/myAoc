import itertools
import re

from helpers import get_locations, read_input  # noqa: F401
from loguru import logger  # noqa: F401
from util import (  # noqa: F401
    extend_list,
    ints,
)

DAY = 2
locations = get_locations(f"day{DAY}")

content = read_input(locations.input_file)
cl = content.split("\n")

# part 1
game_list = [0]
game_results = []
extend_list(game_results, len(cl), True)

for line in cl:
    split = line.split(":")
    game_number = int(ints(split[0])[0])
    game_list.append(game_number)

    games = split[1].split(";")

    for game in games:
        r = 12
        g = 13
        b = 14
        cube_vals = ints(game)
        colors = re.findall("green|blue|red", game)

        for color in colors:
            match color:
                case "green":
                    g -= cube_vals.pop(0)
                case "blue":
                    b -= cube_vals.pop(0)
                case "red":
                    r -= cube_vals.pop(0)

        if (g < 0) or (b < 0) or (r < 0):
            game_results[game_number] = False

wins = itertools.compress(game_list, game_results)
sums = itertools.accumulate(wins)
*_, last = sums
print(f"part 1 sum = {last}")


# part 2

content = read_input(locations.input_file)
cl = content.split("\n")

powers = []

for line in cl:
    split = line.split(":")
    games = split[1].split(";")

    min_red = 0
    min_green = 0
    min_blue = 0
    for game in games:
        r = 0
        g = 0
        b = 0

        cube_vals = ints(game)
        colors = re.findall("green|blue|red", game)

        for color in colors:
            match color:
                case "green":
                    g += cube_vals.pop(0)
                case "blue":
                    b += cube_vals.pop(0)
                case "red":
                    r += cube_vals.pop(0)

        if r > min_red:
            min_red = r
        if g > min_green:
            min_green = g
        if b > min_blue:
            min_blue = b
    powers.append(min_red * min_green * min_blue)


sums = itertools.accumulate(powers)
*_, last = sums
print(f"part 2 sum = {last}")
