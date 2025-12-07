import io
import sys
from datetime import datetime

import pytest

import aoc_service as a

REPEAT = 10


def main():
    date = datetime(year=2025, month=12, day=6)

    if date.day == 4:
        run_one(1527, date, "removed @ check -m", False)
        run_two(
            8690, date, "removed check for @ sign break early for accessible -m", False
        )
    if date.day == 5:
        run_one(613, date, "init", False)
        run_two(336495597913098, date, "init", False)
    if date.day == 6:
        # run_one(5524274308182, date, "init", False)
        run_two(8843673199391, date, "init", True)


def run_one(
    expected, date=datetime.now(), comment="", record_run_result=False, repeat=REPEAT
):
    run(1, expected, date, comment, record_run_result)


def run_two(
    expected, date=datetime.now(), comment="", record_run_result=False, repeat=REPEAT
):
    run(2, expected, date, comment, record_run_result)


def _run_pytest(day: int):
    pytest_output = io.StringIO()
    sys.stdout = pytest_output
    result = pytest.main(
        [f"tests\\test_day{day}.py::test_day{day}example", "--color=yes"]
    )
    sys.stdout = sys.__stdout__
    return result, pytest_output.getvalue()


def run(
    part,
    expected,
    date=datetime.now(),
    comment="",
    record_run_result=False,
    repeat=REPEAT,
):
    year = date.year
    day = date.day
    a.download(date)
    a.generate_scripts(date)

    result, pytest_output = _run_pytest(day)

    if result == pytest.ExitCode.OK:
        print(f"Running Day {day} Part {part} solution...")
        print("======================================================================")
        actual, _ = a.run(day, part, repeat=REPEAT)
        print("======================================================================")
        print("")
        color = a.PART_ONE_COLOR if part == 1 else a.PART_TWO_COLOR
        assert expected == actual, (
            f"Day {day} Part {part} Failed! {a.RESET}Expected = {color}{expected}{a.RESET}; Actual = {a.ORANGE}{actual}{a.RESET}"
        )
        if record_run_result:
            print(f"Running Day{day} Part {part} solution {repeat} times...")
            actual, avg_run_time = a.run(day, part, repeat)
            a.record_run_result(year, day, part, avg_run_time, comment)
            print("")
    else:
        print(pytest_output)


if __name__ == "__main__":
    main()
