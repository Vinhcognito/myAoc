from helpers import get_locations, read_input

DAY = 13

locations = get_locations(f"day{DAY}")

content = read_input(locations.input_file)
patterns = content.split("\n\n")


def check_mirror(li: list[str], idx: int) -> bool:
    for i in range(min([idx + 1, len(li) - (idx + 1)])):
        str1 = li[idx - i]
        str2 = li[idx + 1 + i]
        if str1 == str2:
            continue
        else:
            return False
    return True


def get_diff(str1: str, str2: str) -> int:
    diff_count = 0
    for i, c in enumerate(str1):
        if str1[i] == str2[i]:
            continue
        else:
            diff_count += 1
    return diff_count


def check_smudge(li: list[str], idx: int) -> bool:
    # this could definitely find the orig and the smudge mirror
    diff_count = 0
    for i in range(min([idx + 1, len(li) - (idx + 1)])):
        str1 = li[idx - i]
        str2 = li[idx + 1 + i]
        diff_count += get_diff(str1, str2)
    if diff_count == 1:
        return True
    else:
        return False


part1_sum = 0
part2_sum = 0
for pattern in patterns:
    # look for equivalent adjacent rows and columns
    # get rows

    rows = pattern.split("\n")
    num_rows = len(rows)
    num_cols = len(rows[0])

    h_mirror_idx = None
    v_mirror_idx = None
    v_smudge_idx = None
    h_smudge_idx = None

    # get cols
    cols = ["" for i in range(num_cols)]
    for row in rows:
        for i, value in enumerate(row):
            cols[i] += value

    # search columns
    for i in range(len(cols) - 1):
        if check_mirror(cols, i):
            if v_mirror_idx is None:
                v_mirror_idx = i
                part1_sum += i + 1
        if check_smudge(cols, i):
            if v_smudge_idx is None:
                v_smudge_idx = i
                part2_sum += i + 1

    # search rows
    for i in range(len(rows) - 1):
        if check_mirror(rows, i):
            if h_mirror_idx is None:
                h_mirror_idx = i
                part1_sum += 100 * (i + 1)
        if check_smudge(rows, i):
            if h_smudge_idx is None:
                h_smudge_idx = i
                part2_sum += 100 * (i + 1)

print(f"Part 1 sum = {part1_sum}")
print(f"Part 2 sum = {part2_sum}")
