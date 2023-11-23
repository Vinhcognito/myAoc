from util import *
from collections import namedtuple
from decorators import timer
import re

wipeTerminal()

DAY = 1

INPUT_FOLDER: str = os.path.join(os.getcwd(), "Inputs")

input_path = os.path.join(INPUT_FOLDER, f"day{DAY}.txt")
exampleinput_path = os.path.join(INPUT_FOLDER, f"day{DAY}example.txt")

INPUT = open(input_path, "r", encoding="utf16", errors="ignore")
# EXAMPLE_INPUT = open(exampleinput_path, "r")

content = INPUT.read().strip()
cl = content.split("\n")

printArray(cl)
