from aoc_service import parse_example
from solutions import day3

example_input = "inputs\\day3example.txt"


def test_day3example():
    examples = parse_example(3)

    for example in examples:
        input = example.input_data
        expected_answer_a = example.answer_a
        expected_answer_b = example.answer_b

        assert expected_answer_a == str(day3.part_one(input))
        assert expected_answer_b == str(day3.part_two(input))

    assert len(examples) > 0