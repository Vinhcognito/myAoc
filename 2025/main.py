from datetime import datetime

import pytest

import aoc_service as a

REPEAT = 10


def main():
    date = datetime(year=2025, month=12, day=3)
    # run_one(1527, date, "init with point class fr", True)

    run_two(169709990062889, date, "using list iteration with set of idx", True)


def run_one(
    expected, date=datetime.now(), comment="", record_run_result=False, repeat=REPEAT
):
    run(1, expected, date, comment, record_run_result)


def run_two(
    expected, date=datetime.now(), comment="", record_run_result=False, repeat=REPEAT
):
    run(2, expected, date, comment, record_run_result)


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
    result = pytest.main([f"tests\\test_day{day}.py::test_day{day}example"])
    if result == pytest.ExitCode.OK:
        print(f"Running day{day} part{part} solution...")
        actual, result_time = a.run(day, part)  # type: ignore
        print("")
        assert expected == actual
        if record_run_result:
            print(f"Running day{day} part{part} solution {repeat} times...")
            actual, avg_run_time = a.run(day, part, repeat)  # type: ignore
            a.record_run_result(year, day, part, avg_run_time, comment)
            print("")


if __name__ == "__main__":
    main()
