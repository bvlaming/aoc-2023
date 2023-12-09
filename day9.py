def find_depth(history: list[int], depth: int) -> int:
    if sum(history) == 0:
        return depth
    else:
        history = [history[n + 1] - history[n] for n in range(len(history) - 1)]
        return find_depth(history, depth + 1)


def forecast(history: list[int], acc: int) -> int:
    next_hist = [history[n + 1] - history[n] for n in range(len(history) - 1)]
    if all(not h for h in history):
        return acc
    return forecast(next_hist, acc + history[-1])


def compute_sum(transformer):
    return sum(
        transformer([int(n) for n in line.split()])
        for line in open("input.txt").read().splitlines()
    )


def main():
    with open("data/day9.csv", "r") as file:
        data = file.read().splitlines()

    histories = [[int(x) for x in line.split()] for line in data]

    answer9a = sum(forecast(h, 0) for h in histories)
    print(answer9a)

    def _rev(x: list[int]):
        x.reverse()
        return x

    answer9b = sum(forecast(_rev(h), 0) for h in histories)
    print(answer9b)


if __name__ == "__main__":
    main()
