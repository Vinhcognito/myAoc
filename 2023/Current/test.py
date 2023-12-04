from collections import Counter
from pprint import pprint  # noqa: F401

from decorators import timer
from helpers import Grid, Point, get_locations, read_input  # noqa: F401
from loguru import logger  # noqa: F401
from util import (  # noqa: F401
    clear_terminal,
    extend_list,
    extend_list_2D,
    extend_list_rect,
    ints,
    logger_config,
    print_array,
)


@timer
def run():
    DAY = 4

    locations = get_locations(f"day{DAY}")
    logger.add(f"{locations.log_file}", backtrace=True, diagnose=True)
    logger_config(logger)
    clear_terminal()

    content = read_input(locations.input_file)
    cl = content.split("\n")

    def parse_card(line: str, doPoints=True):
        winstr, numbers = line.split("|")
        win_keys, win_pos = ints(winstr)
        win_dict = dict(zip(win_keys, win_pos))

        num_list, _ = ints(numbers)

        count = 0
        for number in num_list:
            if number in win_dict:
                count += 1

        if doPoints:
            if count == 0:
                return 0
            else:
                return 2 ** (count - 1)
        else:
            return count

    ### part 1
    sum = 0
    for line in cl:
        _, line = line.split(":")
        sum += parse_card(line)

    print(f"Part1: Sum of points = {sum}")

    ### part 2
    card_counter = Counter(range(1, len(cl) + 1))

    for card_number, line in enumerate(cl, 1):
        _, line = line.split(":")
        won = parse_card(line, False)
        for i in range(1, won + 1):
            card_counter[card_number + i] += card_counter[card_number]

    # count number of winning cards
    sum = 0
    for card_num, card_total in card_counter.items():
        if card_num > len(cl) + 1:
            break
        sum += card_total

    print(f"Part2: Total cards on hand = {sum}")


run()
