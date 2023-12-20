from helpers import Point, Vectors, get_locations, read_input

DAY = 16
locations = get_locations(f"day{DAY}")

content = read_input(locations.input_file)
rows = content.split("\n")

grid_width = len(rows[0])
grid_height = len(rows)

grid: dict[Point, str] = {}
for y, row in enumerate(rows):
    for x, c in enumerate(row):
        if c != ".":
            grid[Point(x, y)] = c


def calc_beam(start: Point, dir_vector: Point):
    next_point = start
    while True:
        next_point += dir_vector
        # logger.debug(f"start:{start},dir:{dir_vector},next_pt:{next_point}")
        # wait_for_input()

        # check if this beam has been seen already
        if (next_point, dir_vector) in energized:
            return

        # check grid bounds
        if 0 <= next_point.x <= grid_width - 1 and 0 <= next_point.y <= grid_height - 1:
            energized[(next_point, dir_vector)] = 1
        else:
            return

        if next_point in grid:
            # logger.debug(f"next_pt is in grid:{grid[next_point]}")
            match grid[next_point]:
                case "|":
                    if dir_vector == Vectors.N or dir_vector == Vectors.S:
                        continue
                    else:
                        calc_beam(next_point, Vectors.N)
                        calc_beam(next_point, Vectors.S)
                        return
                case "-":
                    if dir_vector == Vectors.E or dir_vector == Vectors.W:
                        continue
                    else:
                        calc_beam(next_point, Vectors.E)
                        calc_beam(next_point, Vectors.W)
                        return
                case "/":
                    if dir_vector == Vectors.N:
                        calc_beam(next_point, Vectors.E)
                        return
                    if dir_vector == Vectors.E:
                        calc_beam(next_point, Vectors.N)
                        return
                    if dir_vector == Vectors.S:
                        calc_beam(next_point, Vectors.W)
                        return
                    if dir_vector == Vectors.W:
                        calc_beam(next_point, Vectors.S)
                        return
                case "\\":
                    if dir_vector == Vectors.N:
                        calc_beam(next_point, Vectors.W)
                        return
                    if dir_vector == Vectors.E:
                        calc_beam(next_point, Vectors.S)
                        return
                    if dir_vector == Vectors.S:
                        calc_beam(next_point, Vectors.E)
                        return
                    if dir_vector == Vectors.W:
                        calc_beam(next_point, Vectors.N)
                        return
        else:
            continue


energized: dict[tuple[Point, Point]] = {}


def get_num_energized(dict) -> int:
    li = list(dict.keys())
    li.sort(key=lambda tup: (tup[0].y, tup[0].x))
    unique_points = list(set([tup[0] for tup in li]))
    return len(unique_points)


# part 1
calc_beam(Point(-1, 0), Vectors.E)
print(f"Part 1: Number of energized tiles is {get_num_energized(energized)}")

# Part 2
results: dict[Point, int] = {}
# check N,S
for x in range(0, grid_width):
    point = Point(x, -1)
    energized = {}
    calc_beam(point, Vectors.S)
    results[point] = get_num_energized(energized)

    point = Point(x, grid_height)
    energized = {}
    calc_beam(point, Vectors.N)
    results[point] = get_num_energized(energized)

# check E,W
for y in range(0, grid_height):
    point = Point(-1, y)
    energized = {}
    calc_beam(point, Vectors.E)
    results[point] = get_num_energized(energized)

    point = Point(grid_width, y)
    energized = {}
    calc_beam(point, Vectors.W)
    results[point] = get_num_energized(energized)

max = max(results.values())

print(f"Part 2: Max Number of energized tiles is {max}")
