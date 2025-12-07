from aoc_service import parse_example
from solutions import day6

example_input = "inputs\\day6example.txt"


def test_day6example():
    examples = parse_example(6)

    for example in examples:
        input = example.input_data
        expected_answer_a = example.answer_a
        expected_answer_b = example.answer_b

        assert expected_answer_a == str(day6.part_one(input))
        assert expected_answer_b == str(day6.part_two(input))

    assert len(examples) > 0