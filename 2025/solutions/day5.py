from dataclasses import dataclass


@dataclass
class FreshRange:
    start: int
    stop: int

    def is_fresh(self, id: int) -> bool:
        if self.start <= id <= self.stop:
            return True
        return False

    def total(self) -> int:
        return self.stop + 1 - self.start

    def __lt__(self, other: FreshRange):
        return self.start < other.start

    def __le__(self, other: FreshRange):
        return self.start <= other.start

    def __gt__(self, other: FreshRange):
        return self.start > other.start

    def __ge__(self, other: FreshRange):
        return self.start >= other.start


def part_one(input: str):
    lines = input.strip().split("\n")

    linebreak = 0
    ranges: list[FreshRange] = []

    # ranges
    for line in lines:
        linebreak += 1
        if line == "":
            break
        start, end = line.split("-")

        ranges.append(FreshRange(int(start), int(end)))

    # ids
    counter = 0
    for id in lines[linebreak:]:
        for range in ranges:
            if range.is_fresh(int(id)):
                counter += 1
                break

    return counter


def part_two(input: str):
    lines = input.strip().split("\n")

    ranges: list[FreshRange] = []

    # ranges
    for line in lines:
        if line == "":
            break
        start, end = line.split("-")

        new = FreshRange(int(start), int(end))

        ranges.append(new)

    ranges.sort()

    # check for range intersections

    cur_stop = 0
    sum = 0
    for fresh in ranges:
        if fresh.start <= cur_stop:
            sum -= cur_stop - fresh.start + 1
            # print(f"-{cur_stop - fresh.start + 1}+{fresh.total()}")
            cur_stop = max(fresh.stop, cur_stop)
            sum += fresh.total()
            # print(f"sum:{sum}")

            if fresh.stop < cur_stop:
                sum += cur_stop - fresh.stop
                # print(f"\taddendum:{cur_stop - fresh.stop} = {sum}")
        else:
            cur_stop = fresh.stop
            sum += fresh.total()
            # print(f"sum:{sum}")

    # print(sum)

    return sum


# 336495597913098

# 3 - 5               3
# 10 - 14   +5        8
# 12 - 18   -3 + 7 => 12
# 16 - 20   -3 + 5 => 14

# 3 - 5               3
# 3 - 20    -3 + 18   18
# 5 - 14    -16 +10   12
# 12 - 18   -9 + 7 => 10
# 16 - 20   -5 + 5 => 10
