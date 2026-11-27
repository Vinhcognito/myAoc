from helpers import Point, Vectors, get_locations, read_input

DAY = 14

locations = get_locations(f"day{DAY}")

content = read_input(locations.example_file)
rows = content.split("\n")
grid_width = len(rows[0])
grid_height = len(rows)


def move_rock(point: Point, dir_vector: Point):
    if point in grid:
        if grid[point] == "O":
            while True:
                # boundary check
                if (
                    0 <= point.x + dir_vector.x <= grid_width
                    and 0 <= point.y + dir_vector.y <= grid_height
                ):
                    # blockage check
                    if (
                        grid.get(point + dir_vector, ".") != "#"
                        and grid.get(point + dir_vector, ".") != "O"
                    ):
                        grid[point + dir_vector] = grid[point]
                        grid.pop(point)
                        point += dir_vector
                    else:
                        return
                else:
                    return


def tilt_grid(dir_vector: Point):
    match dir_vector:
        case Vectors.N:
            start = 1
            stop = grid_height
            step = +1
            vert = True
        case Vectors.S:
            start = grid_height - 1
            stop = 0
            step = -1
            vert = True
        case Vectors.W:
            start = 1
            stop = grid_width
            step = +1
            vert = False
        case Vectors.E:
            start = grid_width - 1
            stop = 0
            step = -1
            vert = False
        case _:
            return

    if vert:
        for y in range(start, stop, step):
            for x in range(0, grid_width):
                move_rock(Point(x, y), dir_vector)
    else:
        for x in range(stop, stop, step):
            for y in range(0, grid_height):
                move_rock(Point(x, y), dir_vector)


def calculate_load() -> int:
    load = 0
    for point in grid.keys():
        if grid[point] == "O":
            load += grid_height - point.y
    return load


# parse input
grid: dict[Point, str] = {}
for y, row in enumerate(rows):
    for x, c in enumerate(row):
        if c != ".":
            grid[Point(x, y)] = c

tilt_grid(Vectors.N)
print(f"Part 1: The Total load is: {calculate_load()}")
