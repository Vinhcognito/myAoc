from __future__ import annotations

__all__ = [
    "read_input",
    "staticproperty",
    "Locations",
    "get_locations",
    "Point",
    "Vectors",
    "VectorDicts",
    "Grid",
]
import math
import os
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path

INPUT_FOLDER: str = os.path.join(os.getcwd(), "Inputs")


def read_input(file_path: str):
    """reads the file and returns the content"""

    try:
        input = open(file_path, "r", encoding="utf16", errors="ignore")
        return input.read().strip()
    except UnicodeError:
        print("Unicode Error")

    try:
        input = open(file_path, "r", errors="ignore")
        return input.read().strip()
    except UnicodeError:
        print("Unicode Error")


class staticproperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget()


@dataclass
class Locations:
    """Dataclass for storing various location properties"""

    script_name: str
    script_dir: Path
    input_dir: Path
    output_dir: Path
    log_file: Path
    log_file_timestamp: Path
    input_file: Path
    example_file: Path


def get_locations(script_name, folder="") -> Locations:
    """Set various paths, based on the location of the calling script."""
    current_directory = os.getcwd()
    script_dir = Path(Path().resolve(), folder, "Current")
    input_dir = Path(current_directory, "Inputs")
    output_dir = Path(current_directory, "logs")
    log_file = Path(output_dir, f"{script_name}.log")
    log_file_timestamp = Path(
        output_dir, f"{script_name}-{datetime.now().strftime("%Y-%m-%d-%H%M")}.log"
    )
    input_file = Path(input_dir, f"{script_name}.txt")
    example_file = Path(input_dir, f"{script_name}example.txt")

    return Locations(
        script_name,
        script_dir,
        input_dir,
        output_dir,
        log_file,
        log_file_timestamp,
        input_file,
        example_file,
    )


@dataclass(frozen=True)
class Point:
    """Class for storing a point x,y coordinate of ints"""

    x: int
    y: int

    def __add__(self, other: Point):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other: Point):
        """(x, y) * (a, b) = (xa, yb)"""
        return Point(self.x * other.x, self.y * other.y)

    def __sub__(self, other: Point):
        return self + Point(-other.x, -other.y)

    def __eq__(self, other: Point) -> bool:
        return self.x == other.x and self.y == other.y

    # Comparisons by distance to origin

    def __lt__(self, other: Point):
        return self.distance_to_origin(self) < self.distance_to_origin(other)

    def __le__(self, other: Point):
        """compare by distance to origin"""
        return self.distance_to_origin(self) <= self.distance_to_origin(other)

    def __gt__(self, other: Point):
        """compare by distance to origin"""
        return self.distance_to_origin(self) > self.distance_to_origin(other)

    def __ge__(self, other: Point):
        """compare by distance to origin"""
        return self.distance_to_origin(self) >= self.distance_to_origin(other)

    @staticproperty
    def origin() -> Point:
        """(0,0)"""
        return Point(0, 0)

    def yield_neighbours(self, include_diagonals=True, include_self=False):
        """Generator to yield neighbouring Points"""

        deltas: list
        if not include_diagonals:
            deltas = [
                vector.value
                for vector in Vectors
                if abs(vector.value[0]) != abs(vector.value[1])
            ]
        else:
            deltas = [vector.value for vector in Vectors]

        if include_self:
            deltas.append((0, 0))

        for delta in deltas:
            yield Point(self.x + delta[0], self.y + delta[1])

    def neighbours(self, include_diagonals=True, include_self=False) -> list[Point]:
        """Return all the neighbours, with specified constraints.
        It wraps the generator with a list."""
        return list(self.yield_neighbours(include_diagonals, include_self))

    def get_specific_neighbours(self, directions: list[Vectors]) -> list[Point]:
        """Get neighbours, given a specific list of allowed locations"""
        return [(self + Point(*vector.value)) for vector in list(directions)]

    @staticmethod
    def manhattan_distance(a_point: Point) -> int:
        """Return the Manhattan distance value of this vector"""
        return sum(abs(coord) for coord in asdict(a_point).values())

    def manhattan_distance_from(self, other: Point) -> int:
        """Manhattan distance between this Vector and another Vector"""
        diff = self - other
        return Point.manhattan_distance(diff)

    @staticmethod
    def distance_to_origin(point: Point):
        return Point.distance_between(point, Point.origin)

    @staticmethod
    def distance_between(p1: Point, p2: Point) -> float:
        """returns distance between two Points"""
        return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

    def distance_from(self, other: Point) -> float:
        """returns distance between this Point and another Point"""
        return self.distance_between(self, other)

    def heading_from(self, starting_point: Point = origin) -> float:
        """gives degree heading to self from a given origin"""
        rel_self = self - starting_point
        return math.atan(rel_self.y / rel_self.x) * 360 / math.pi

    def __str__(self):
        return f"P({round(self.x,2)},{round(self.y,2)})"

    def __repr__(self):
        return f"Point({self.x},{self.y})"


class Vectors(Enum):
    """Enumeration of 8 directions.
    Note: y axis increments in the North direction, i.e. N = (0, 1)"""

    N = (0, 1)
    NE = (1, 1)
    E = (1, 0)
    SE = (1, -1)
    S = (0, -1)
    SW = (-1, -1)
    W = (-1, 0)
    NW = (-1, 1)

    @property
    def y_inverted(self):
        """Return vector, but with y-axis inverted. I.e. N = (0, -1)"""
        x, y = self.value
        return (x, -y)


class VectorDicts:
    """Contains constants for Vectors"""

    ARROWS = {
        "^": Vectors.N.value,
        ">": Vectors.E.value,
        "v": Vectors.S.value,
        "<": Vectors.W.value,
    }

    DIRS = {
        "U": Vectors.N.value,
        "R": Vectors.E.value,
        "D": Vectors.S.value,
        "L": Vectors.W.value,
    }

    NINE_BOX: dict[str, tuple[int, int]] = {
        # x, y vector for adjacent locations
        "tr": (1, 1),
        "r": (1, 0),
        "br": (1, -1),
        "b": (0, -1),
        "bl": (-1, -1),
        "l": (-1, 0),
        "tl": (-1, 1),
        "t": (0, 1),
    }


class Grid:
    """2D grid of point values."""

    def __init__(self, grid_array: list) -> None:
        self._array = grid_array
        self._width = len(self._array[0])
        self._height = len(self._array)

    def value_at_point(self, point: Point) -> int:
        """The value at this point"""
        return self._array[point.y][point.x]

    def set_value_at_point(self, point: Point, value: int):
        self._array[point.y][point.x] = value

    def valid_location(self, point: Point) -> bool:
        """Check if a location is within the grid"""
        if 0 <= point.x < self._width and 0 <= point.y < self._height:
            return True

        return False

    @property
    def width(self):
        """Array width (cols)"""
        return self._width

    @property
    def height(self):
        """Array height (rows)"""
        return self._height

    def all_points(self) -> list[Point]:
        points = [Point(x, y) for x in range(self.width) for y in range(self.height)]
        return points

    def rows_as_str(self):
        """Return the grid"""
        return ["".join(str(char) for char in row) for row in self._array]

    def cols_as_str(self):
        """Render columns as str. Returns: list of str"""
        cols_list = list(zip(*self._array))
        return ["".join(str(char) for char in col) for col in cols_list]

    def __repr__(self) -> str:
        return f"Grid(size={self.width}*{self.height})"

    def __str__(self) -> str:
        return "\n".join("".join(map(str, row)) for row in self._array)
