import importlib
import os
import re
import subprocess
import time
import timeit
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean

import db

PERSON = "v"

# 256-color ANSI escape codes
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
ORANGE = "\x1b[38;5;208m"  # Orange from 256-color palette
RESET = "\x1b[0m"

PART_ONE_COLOR = CYAN
PART_TWO_COLOR = GREEN


def download(current_date=datetime.now()):
    # Get current date
    # print(current_date)

    # Ensure we're in December
    if current_date.month != 12:
        print("Not in December, exiting.")
        return

    # Loop through days 1 to current day
    for day in range(1, current_date.day + 1):
        # Construct filenames
        input_filename = f"inputs\\day{day}.txt"
        example_filename = f"inputs\\day{day}example.txt"

        # Download puzzle input
        if not os.path.exists(input_filename):
            command = f"aocd {day} {current_date.year} > {input_filename}"
            subprocess.run(command, shell=True, check=True)
            print(f"Downloaded input for day {day}, year {current_date.year}")

        # Download example
        if not os.path.exists(example_filename):
            command = f"aocd {day} {current_date.year} --example > {example_filename}"
            subprocess.run(command, shell=True, check=True)
            print(f"Downloaded example for day {day}, year {current_date.year}")


def generate_scripts(date=datetime.now()):
    # Generate test script
    if date.month != 12:
        print("Not in December, exiting.")
        return

    day = date.day
    test_fn = f"test_day{day}.py"
    test_fpath = f"tests\\{test_fn}"

    content = f"""
from aoc_service import parse_example
from solutions import day{day}

example_input = "inputs\\\\day{day}example.txt"


def test_day{day}example():
    examples = parse_example({day})

    for example in examples:
        input = example.input_data
        expected_answer_a = example.answer_a
        expected_answer_b = example.answer_b

        assert expected_answer_a == str(day{day}.part_one(input))
        assert expected_answer_b == str(day{day}.part_two(input))

    assert len(examples) > 0
    
    """
    if not Path(test_fpath).exists():
        with open(test_fpath, "w") as f:
            f.write(content.strip())

    # Generate solution script
    solution_fpath = f"solutions\\day{day}.py"
    solution_content = """
def part_one(input: str):
    return "-"


def part_two(input: str):
    return "-"
    """
    if not Path(solution_fpath).exists():
        with open(solution_fpath, mode="w") as f:
            f.write(solution_content.strip())


def submit_solution():
    pass


def record_run_result(
    year: int,
    day: int,
    part: int,
    result_time: float,
    comment: str = "",
    person=PERSON,
    timestamp: datetime = datetime.now(timezone.utc),
):
    with open(f"solutions\\day{day}.py", "r") as f:
        code = f.read().strip()
        db.create_record(year, day, part, result_time, timestamp, comment, person, code)


def run(day: int, part: int, repeat: int = 1):
    try:
        module = importlib.import_module(f"solutions.day{day}")
        func = getattr(module, "part_one" if part == 1 else "part_two")

        with open(f"inputs\\day{day}.txt", "r") as f:
            input_text = f.read().strip()

        start = time.perf_counter()
        answer = func(input_text)
        end = time.perf_counter()
        result_time = end - start

        color = PART_ONE_COLOR if part == 1 else PART_TWO_COLOR
        if repeat > 1:

            def to_run():
                func(input_text)

            result_time = mean(timeit.repeat(to_run, repeat=repeat, number=1))
            print(
                f"Day {day} {color}Part {part}{RESET} Answer: {color}{answer}{RESET}, Avg Time ({repeat}): {color}{result_time:.6f}{RESET} seconds"
            )
        else:
            print(
                f"Day {day} {color}Part {part}{RESET} Answer: {color}{answer}{RESET}, Time: {color}{result_time:.6f}{RESET} seconds"
            )

        return answer, result_time
    except ImportError as e:
        print(f"Error importing module: {e}")

    except AttributeError:
        print("Module to import not found")
    return None, 0.0


def parse_example(day: int):
    with open(f"inputs\\day{day}example.txt") as f:
        input = f.read().strip()
        lines = input.split("\n")[2:]

        examples = []

        for line in lines:
            example_title_line = re.findall(r"(Example data .*) -", line)
            if len(example_title_line):
                examples.append(Example())
            elif line.startswith(
                "--------------------------------------------------------------------------------"
            ):
                pass
            elif line.startswith("answer_a"):
                examples[-1].answer_a = line.lstrip("answer_a: ")
            elif line.startswith("answer_b"):
                examples[-1].answer_b = line.lstrip("answer_b: ")
            else:
                examples[-1].input_lines.append(line)

        return examples


@dataclass
class Example:
    input_lines: list[str] = field(default_factory=list)
    answer_a: str = ""
    answer_b: str = ""

    @property
    def input_data(self):
        return "\n".join(self.input_lines)
