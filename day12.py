import itertools
import re


def parse_data(lines: list[str]) -> list[tuple[str, list[int]]]:
    data = []
    for line in lines:
        springs, values = line.split(" ")
        spring_lengths = [int(v) for v in values.split(",")]
        data += [(springs, spring_lengths)]
    return data


def regex_spring(spring_lengths: list[int]) -> str:
    rgx = "^(\.*)"
    for n, length in enumerate(spring_lengths):
        if n < len(spring_lengths) - 1:
            rgx += "(#{" + str(length) + "})(\.+)"
        else:
            rgx += "(#{" + str(length) + "})(\.*)"
    return rgx


def generate_combinations(input: str, x: int):
    # In the input, replace x ?'s by # and the rest by .
    question_mark_idx = [n for n, char in enumerate(input) if char == "?"]

    combinations = itertools.combinations(question_mark_idx, x)

    results = []

    for combo in combinations:
        list_input = list(input)
        for index in combo:
            list_input[index] = "#"
        output = []
        for c in list_input:
            c = "." if c == "?" else c
            output += [c]
        output = "".join(output)
        results += [output]

    return results


def solutions(springs: str, spring_lengths: list[int]) -> int:
    total_springs = sum(spring_lengths)
    springs_to_replace = total_springs - len([c for c in springs if c == "#"])
    combos_to_check = generate_combinations(springs, springs_to_replace)
    regex_check = regex_spring(spring_lengths)

    return len([s for s in combos_to_check if re.match(regex_check, s)])


def unfold(spring_data: str, factor: int) -> str:
    spring_data_new = []
    for n in range(factor - 1):
        spring_data_new += [spring_data] + ["?"]
    spring_data_new += [spring_data]

    return "".join(spring_data_new)


def main():
    with open("data/day12test.csv", "r") as file:
        data = file.read().splitlines()

    spring_data = parse_data(data)
    answer_a = sum(solutions(sd[0], sd[1]) for sd in spring_data)
    print(answer_a)


if __name__ == "__main__":
    main()
