import math


def part_one(input: str):
    lines = input.split(",")
    sum = 0
    for entry in lines:
        first, last = entry.split("-")

        # check for sequence doubling
        for num in range(int(first), int(last) + 1):
            s = str(num)
            if len(s) % 2 != 0:
                continue
            split = int(len(s) / 2)
            if s[:split] == s[split:]:
                sum += num
    return sum


def part_two(input: str):
    lines = input.split(",")
    sum = 0

    for entry in lines:
        first, last = entry.split("-")

        for num in range(int(first), int(last) + 1):
            s = str(num)
            if check(s):
                sum += num

    return sum


def check(num: str) -> bool:
    for factor in range(1, math.floor(len(num) / 2)):
        flag = True
        if len(num) % factor == 0:
            li = []
            for i in range(int(len(num) / factor)):
                li.append(num[i * factor : (i + 1) * factor])
            if len(li) == 1:
                continue
            for i in range(len(li)):
                if li[0] != li[i]:
                    flag = False
            if flag:
                return True

    return False
