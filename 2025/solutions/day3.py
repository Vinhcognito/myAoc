def part_one(input: str):
    banks = input.strip().split("\n")

    sum = 0
    for bank in banks:
        li = list(bank)
        li.sort()
        one = li[-1]
        two = li[-2]

        li = list(bank)

        # check if last in bank, use second last
        if li.index(one) == len(li) - 1:
            one = two

        result = 0
        for i in range(li.index(one) + 1, len(li)):
            if result < int(one + li[i]):
                result = int(one + li[i])
        sum += result

    return sum


def part_two(input: str):
    banks = input.strip().split("\n")

    sum = 0
    for bank in banks:
        result = ""
        used = set()
        for i in range(12, 0, -1):
            max, idx = find_max(bank, i, used)
            used.add(idx)
            result += max
        print(result)
        sum += int(result)
    return sum


def find_max(s: str, i: int, used: set) -> tuple[str, int]:
    """returns max, idx"""
    li = list(s)
    result = 0
    index = 0
    if len(used) > 0:
        maxused = max(used)
    else:
        maxused = 0
    for idx, n in enumerate(li):
        if (
            int(n) > result
            and idx not in used
            and idx + i - 1 < len(s)
            and idx >= maxused
        ):
            result = int(n)
            index = idx
            if result == 9:
                break

    return str(result), index
