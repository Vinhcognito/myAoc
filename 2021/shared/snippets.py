start = min(coord for coord, char in grid.items() if char == ".")
end = max(coord for coord, char in grid.items() if char == ".")


print(
    "\n".join(
        "".join(grid.get((x, y), " ") for x in range(xmin, xmax + 1))
        for y in range(ymin, ymax + 1)
    )
)
