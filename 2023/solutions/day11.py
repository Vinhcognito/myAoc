from itertools import combinations

from helpers import Point, get_locations, read_input

DAY = 11

locations = get_locations(f"day{DAY}")

content = read_input(locations.input_file)
rows = content.split("\n")

empty_rows = []
empty_cols = []
cols = ["" for i in range(len(rows[0]))]
galaxies = []

for y, row in enumerate(rows):
    # find empty rows
    if row.find("#") == -1:
        empty_rows.append(y)
    # make col strings
    for x, c in enumerate(row):
        cols[x] += c
        if c == "#":
            galaxies.append(Point(x, y))

# find empty cols
for x, col in enumerate(cols):
    if col.find("#") == -1:
        empty_cols.append(x)


def get_dist(start: Point, end: Point, multiplier: int = 1):
    dist = abs(end.y - start.y) + abs(end.x - start.x)
    for row_num in empty_rows:
        if min(start.y, end.y) <= row_num <= max(start.y, end.y):
            dist += 1 * multiplier
    for col_num in empty_cols:
        if min(start.x, end.x) <= col_num <= max(start.x, end.x):
            dist += 1 * multiplier
    return dist


result = 0
for pair in combinations(galaxies, 2):
    result += get_dist(pair[0], pair[1])

print(f"Part 1: sum of distances is {result}")

# part 2

multiplier = 1000000 - 1

result = 0
for pair in combinations(galaxies, 2):
    result += get_dist(pair[0], pair[1], multiplier)

print(f"Part 2: sum of distances is {result}")
