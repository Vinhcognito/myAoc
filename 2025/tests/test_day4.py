from aoc_service import parse_example
from solutions import day4

example_input = "inputs\\day4example.txt"


def test_day4example():
    examples = parse_example(4)

    for example in examples:
        input = example.input_data
        expected_answer_a = example.answer_a
        expected_answer_b = example.answer_b

        assert expected_answer_a == str(day4.part_one(input))
        assert expected_answer_b == str(day4.part_two(input))

    assert len(examples) > 0