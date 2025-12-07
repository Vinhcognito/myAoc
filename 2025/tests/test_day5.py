from aoc_service import parse_example
from solutions import day5

example_input = "inputs\\day5example.txt"


def test_day5example():
    examples = parse_example(5)

    for example in examples:
        input = example.input_data
        expected_answer_a = example.answer_a
        expected_answer_b = example.answer_b

        # assert expected_answer_a == str(day5.part_one(input))
        assert expected_answer_b == str(day5.part_two(input))

    assert len(examples) > 0
