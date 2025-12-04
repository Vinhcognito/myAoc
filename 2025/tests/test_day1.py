from aoc_service import parse_example
from solutions import day1

example_input = "inputs\\day1example.txt"


def test_day1example():
    examples = parse_example(1)

    for idx, example in enumerate(examples):
        part = idx + 1
        input = example.input_data
        expected_answer_a = example.answer_a
        expected_answer_b = example.answer_b

        if part == 1:
            assert expected_answer_a == str(day1.part_one(input))

        if part == 2:
            assert expected_answer_b == str(day1.part_two(input))

    assert len(examples) > 0