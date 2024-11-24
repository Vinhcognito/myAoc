from functools import reduce

from helpers import get_locations, read_input

DAY = 9

locations = get_locations(f"day{DAY}")

content = read_input(locations.input_file)
cl = content.split("\n")


def is_all_equal(li):
    return len(set(li)) <= 1


p1_values = []
p2_values = []

for line in cl:
    li = []
    diff_flag = False
    li.append([int(num) for num in line.split(" ")])
    for level in range(len(li[0])):
        # append differences
        li.append([])
        for idx in range(0, len(li[level]) - 1):
            li[level + 1].append(li[level][idx + 1] - li[level][idx])
        # check all in list of diffs is equal
        if is_all_equal(li[level + 1]):
            # part 1
            p1_result = 0
            for i in range(len(li)):
                p1_result += li[i][-1]
            p1_values.append(p1_result)

            # part 2
            p2_result = li[len(li) - 1][0]
            for tier in range(len(li) - 1, 0, -1):
                p2_result = li[tier - 1][0] - p2_result
            p2_values.append(p2_result)
            break


p1_sum = reduce(lambda x, y: x + y, p1_values)
p2_sum = reduce(lambda x, y: x + y, p2_values)
print(f" part 1 sum = {p1_sum}")
print(f" part 2 sum = {p2_sum}")
