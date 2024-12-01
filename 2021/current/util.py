import math
import os
import sys
from functools import cache

import loguru
from loguru import logger

log = logger


__all__ = [
    "logger_config",
    "get_factors",
    "to_base_n",
    "sign",
    "clear_terminal",
    "ints",
    "strs",
    "extend_list",
    "extend_list_2D",
    "extend_list_rect",
    "print_array",
    "text2int",
]


def logger_init():
    log.remove(0)
    logger_config(log)


def logger_enable(loguru_logger, filename):
    """enables file output to the logs folder"""
    logger_config(loguru_logger, f"logs\\{filename}.log")


def logger_config(loguru_logger, sink=sys.stderr):
    """setup loguru with a modified console printout"""
    # for: day1.py:<module>
    #  <cyan>{file}</cyan>:<cyan>{function}</cyan>

    # for time: {time:mm:ss.ms}

    loguru_logger.add(
        sink,
        level="DEBUG",
        format="{elapsed}| <level>{level: <8}</level> |:<bold><green>{line}</green></bold> - <level>{message}</level>",
        filter=None,
        colorize=None,
        serialize=False,
        backtrace=True,
        diagnose=True,
        enqueue=False,
        context=None,
        catch=True,
    )


@cache
def get_factors(num: int) -> set[int]:
    """Gets the factors for a given number. Returns a set[int] of factors.
    # E.g. when num=8, factors will be 1, 2, 4, 8"""
    factors = set()

    # Iterate from 1 to sqrt of num,
    # since a larger factor of num must be a multiple of a smaller factor already checked
    for i in range(1, int(num**0.5) + 1):  # e.g. with num=8, this is range(1, 3)
        if (
            num % i == 0
        ):  # if it is a factor, then dividing num by it will yield no remainder
            factors.add(i)
            factors.add(num // i)

    return factors


def wait_for_input():
    """function for pausing a stream of printouts until user input is received"""
    input("")


def to_base_n(number: int, base: int):
    """Convert any integer number into a base-n string representation of that number.
    E.g. to_base_n(38, 5) = 123

    Args:
        number (int): The number to convert
        base (int): The base to apply

    Returns:
        [str]: The string representation of the number
    """
    ret_str = ""
    curr_num = number
    while curr_num:
        ret_str = str(curr_num % base) + ret_str
        curr_num //= base

    return ret_str if number > 0 else "0"


def sign(x):
    """Returns -1 or +1 corresponding to the sign of x"""
    return int(math.copysign(1, x))


def clear_terminal(s: str = "=", num: int = 80, clear: bool = False):
    """Use to put a line of separators (str) of length (num) in the terminal"""
    temp = s * num
    if clear:
        os.system("cls" if os.name == "nt" else "clear")
    print("\n" + temp)
    return


def ints(string: str, digits: int = 0, signs: bool = True):
    """Returns list of all integers in string

    Searches string for connected integers flanked by non integer characters, use digits=1 for each item to be 1 digit in length

    ### digits (0):\n
        max number of digits that each int is allowed to have
        0 -> unlimited digits\n
    ### signs (True):\n
        When False: will ignore negative (-) signs that may be in front of integers
    """
    intlist = []
    tempString = []
    poslist = []
    count = 0
    for idx, c in enumerate(string):
        if str(c).isnumeric():
            if signs is True and idx > 0:
                if string[idx - 1] == "-":
                    tempString.append("-")
            tempString.append(c)
            count += 1
            if count == digits:
                intlist.append(int("".join(tempString)))
                poslist.append(idx - len(str(intlist[-1])))
                tempString = []
                count = 0
        else:
            if count >= 1:
                intlist.append(int("".join(tempString)))
                poslist.append(idx - len(str(intlist[-1])))
                tempString = []
                count = 0

    if count >= 1:
        intlist.append(int("".join(tempString)))
        poslist.append(idx - len(str(intlist[-1])))
    return intlist, poslist


def strs(
    string: str,
    maxchars: int = 0,
):
    """Returns list of all strings in string

    Searches string for connected alphabetic chars flanked by non alpha  characters

    ### maxchars (0):\n
        max number of chars that each string is allowed to have
        0 -> unlimited chars
    """
    strlist = []
    tempString = []
    count = 0
    for idx, c in enumerate(string):
        if str(c).isalpha():
            tempString.append(c)
            count += 1
            if count == maxchars:
                strlist.append("".join(tempString))
                tempString = []
                count = 0
        else:
            if count >= 1:
                strlist.append("".join(tempString))
                tempString = []
                count = 0

    if count >= 1:
        strlist.append("".join(tempString))
    return strlist


def extend_list(input_list: list, index: int, fill=0):
    """Returns list extended for index specified to exist, filled with specified char

    index:
        index that input_list will be extended to
    fill:
        default value for newly created indexes in list
    """
    temp_list = input_list
    while True:
        try:
            # try to access list index
            temp = temp_list[index]  # noqa: F821, F841
            break
        except IndexError:
            # if list not lot enough
            temp_list.append(fill)  # noqa: F821
        # is this needed?
        """
        except TypeError:
            
            temp_list.append(input_list)
            return extend_list(temp_list, index, fill)
        """
    return temp_list


def extend_list_2D(input_list: list, index1: int, index2: int, fill=0):
    """Copies contents of a list and returns it extended to just enough
    with default values = (fill)  for  li[index1][index2] to exist"""
    temp_list = input_list
    try:
        temp = temp_list[index1][index2]  # noqa: F841
    except IndexError:
        # append until index1 satisfied
        while len(temp_list) <= index1:
            temp_list.append([fill])
        # extend slice at li[index1] to satisfy index2
        temp_list[index1] = extend_list(temp_list[index1], index2, fill)
    except TypeError:
        while len(temp_list) <= index1:
            temp_list.append([fill])
        temp_list[index1] = extend_list(temp_list[index1], index2, fill)
    return temp_list


def extend_list_rect(li: list, index1: int = 1, index2: int = 1, fill=0):
    """Copies contents of a list and returns it extended so that all possible indices
    within [0,index1]X[0,index2] are created with initial values = (fill)"""
    temp_list = li
    for i in range(index1 + 1):
        temp_list = extend_list_2D(temp_list, i, index2, fill)
    return temp_list


def print_array(
    input_array: list,
    hRange=[],
    vRange=[],
    tight=True,
    revX=False,
    revY=False,
    true="1",
    false="0",
    mappings: dict = {},
    title: str = "",
    **kwargs,
):
    """Prints contents of a 2D list into the terminal

    Args:

    ### hRange,vRange:list[int,int]
        specify starting and ending index of values to print. able to accept None in place of int
    ### tight (True):
        values are printed with no comma separation and with replacements specified from true and false parameters and any additional keyword pairs
        False: values are printed as values only with a comma separation
    ### revX (False):
        Specifies whether the horizontal values are printed in ascending or descending (True), index order
    ### revY (False):
        Specifies whether the vertical values are printed in ascending (False) or descending (True), index order
    ### true (1),false (0):
        true replaces all True or 1 values with the str specified by true\n
        all False or 0 values with the str specified by false
    ### mappings:
        a dictionary of {value:replacement} mappings that the function will use
            In addition to true,false, kwargs parameters\n
            mapping gets priority if there are conflicts
    \n
    #### additional keyword arguments:
    keyword='string'
    e.g. two='$'
        keywords will be converted from text to integer and will be used to replace instances of that integer to the specified string when printing tight=true
    """
    replace = kwargs.copy()
    for k in list(replace):
        replace[text2int(k)] = replace[k]
    replace[1] = true
    replace[0] = false
    replace = replace | mappings

    if hRange == []:
        hRange = [0, len(input_array[0]) - 1]
    if vRange == []:
        vRange = [0, len(input_array) - 1]

    if hRange[0] is None:
        hRange[1] = 0
    if hRange[1] is None:
        hRange[1] = len(input_array[0]) - 1

    if vRange[1] is None:
        vRange[1] = len(input_array) - 1
    if vRange[0] is None:
        vRange[1] = 0

    param_str = f"[{hRange[0]},{hRange[1]}] to [{vRange[0]},{vRange[1]}] revX={revX} revY={revY}"

    if tight:
        print(f"\ntitle printing tight from {param_str}\n")
    else:
        print(f"\n{title} printing comma separated values from {param_str}\n")

    match revY, revX:
        case False, False:
            for x in range(vRange[0], vRange[1] + 1):
                printBuffer = []
                for y in range(hRange[0], hRange[1] + 1):
                    if tight:
                        if input_array[x][y] in replace:
                            printBuffer.append(replace[input_array[x][y]])
                        else:
                            printBuffer.append(str(input_array[x][y]))
                    else:
                        printBuffer.append(input_array[x][y])
                if tight:
                    print("".join(printBuffer))
                else:
                    print(printBuffer)
        case True, False:
            x = vRange[1]
            while x >= vRange[0]:
                printBuffer = []
                for y in range(hRange[0], hRange[1] + 1):
                    if tight:
                        if input_array[x][y] in replace:
                            printBuffer.append(replace[input_array[x][y]])
                        else:
                            printBuffer.append(str(input_array[x][y]))
                    else:
                        printBuffer.append(input_array[x][y])
                if tight:
                    print("".join(printBuffer))
                else:
                    print(printBuffer)
                x -= 1
        case False, True:
            for x in range(vRange[0], vRange[1] + 1):
                y = hRange[1]
                printBuffer = []
                while y >= hRange[0]:
                    if tight:
                        if input_array[x][y] in replace:
                            printBuffer.append(replace[input_array[x][y]])
                        else:
                            printBuffer.append(str(input_array[x][y]))
                    else:
                        printBuffer.append(input_array[x][y])
                    y -= 1
                if tight:
                    print("".join(printBuffer))
                else:
                    print(printBuffer)
        case True, True:
            x = vRange[1]
            while x >= vRange[0]:
                y = hRange[1]
                printBuffer = []
                while y >= hRange[0]:
                    if tight:
                        if input_array[x][y] in replace:
                            printBuffer.append(replace[input_array[x][y]])
                        else:
                            printBuffer.append(str(input_array[x][y]))
                    else:
                        printBuffer.append(input_array[x][y])
                    y -= 1
                if tight:
                    print("".join(printBuffer))
                else:
                    print(printBuffer)
                x -= 1
    return


def text2int(textnum, numwords={}):
    """
    takes input text description of number (space separated) and returns int of the number
    """
    if not numwords:
        units = [
            "zero",
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
            "ten",
            "eleven",
            "twelve",
            "thirteen",
            "fourteen",
            "fifteen",
            "sixteen",
            "seventeen",
            "eighteen",
            "nineteen",
        ]

        tens = [
            "",
            "",
            "twenty",
            "thirty",
            "forty",
            "fifty",
            "sixty",
            "seventy",
            "eighty",
            "ninety",
        ]

        scales = ["hundred", "thousand", "million", "billion", "trillion"]

        numwords["and"] = (1, 0)
        for idx, word in enumerate(units):
            numwords[word] = (1, idx)
        for idx, word in enumerate(tens):
            numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales):
            numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            raise Exception("Illegal word: " + word)

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current
