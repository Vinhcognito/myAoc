from datetime import datetime

import pytest

import aoc_service as a


def main():
    date = datetime(year=2025, month=12, day=1)
    if date.day == 1:
        run_one("-", date)
        # run_two("-", date)
    elif date.day == 2:
        run("-", "-", date)


def run_one(expected, date=datetime.now(), comment="", record_run_result=True):
    run(1, expected, date, comment, record_run_result)


def run_two(expected, date=datetime.now(), comment="", record_run_result=True):
    run(2, expected, date, comment, record_run_result)


def run(part, expected, date=datetime.now(), comment="", record_run_result=True):
    year = date.year
    day = date.day
    a.download(date)
    a.generate_scripts(date)
    result = pytest.main([f"tests\\test_day{day}.py::test_day{day}example"])
    if result == pytest.ExitCode.OK:
        print(f"Running day{day} part{part} solution...")
        actual, result_time = a.run(day, part) # type: ignore
        assert expected == actual
        if record_run_result:
            a.record_run_result(year, day, part, result_time, comment)


if __name__ == "__main__":
    main()