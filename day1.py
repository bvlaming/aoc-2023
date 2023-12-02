def filter_string1a(line: str) -> int:
    """Filter out non-numerical values and return first and last number."""
    filtered_string = [c for c in line if c.isdigit()]
    return int(filtered_string[0] + filtered_string[-1])


def filter_string1b(line: str) -> int:
    digit_map = {
        "one": "on1ne",
        "two": "tw2wo",
        "three": "th3ee",
        "four": "fo4ur",
        "five": "fi5ve",
        "six": "si6",
        "seven": "se7en",
        "eight": "ei8ght",
        "nine": "ni9ne",
    }
    for k, v in digit_map.items():
        line = line.replace(k, str(v))
    filtered_string = [c for c in line if c.isdigit()]
    return int(filtered_string[0] + filtered_string[-1])


def main():
    with open("data/day1.csv", "r") as file:
        data = file.read().splitlines()

    filtered_data = [filter_string1a(line) for line in data]
    result1a = sum(filtered_data)
    print(result1a)

    filtered_data2 = [filter_string1b(line) for line in data]
    print(sum(filtered_data2))


if __name__ == "__main__":
    main()
