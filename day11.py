from dataclasses import dataclass


@dataclass
class Galaxy:
    x: int
    y: int
    value: str

    def __hash__(self):
        return hash((self.x, self.y))


def parse_grid(lines: list[str]) -> list[Galaxy]:
    points = []
    for y, line in enumerate(lines, start=1):
        for x, value in enumerate(line, start=1):
            if value == "#":
                points += [Galaxy(x, y, value)]
    return points


def expand_universe(galaxies: list[Galaxy], factor: int = 1) -> list[Galaxy]:
    max_x = max(g.x for g in galaxies)
    max_y = max(g.y for g in galaxies)

    empty_x = [x for x in range(1, max_x + 1) if not any(g.x == x for g in galaxies)]
    empty_y = [y for y in range(1, max_y + 1) if not any(g.y == y for g in galaxies)]

    for g in galaxies:
        # count number of empty rows with lower x/y. Add that to its own coordinates
        delta_x = len([x for x in empty_x if g.x >= x])
        delta_y = len([y for y in empty_y if g.y >= y])
        g.x = g.x + (factor - 1) * delta_x
        g.y = g.y + (factor - 1) * delta_y

    return galaxies


def dist(g1: Galaxy, g2: Galaxy) -> int:
    return abs(g1.x - g2.x) + abs(g1.y - g2.y)


def cumul_distances(galaxies: list[Galaxy]) -> int:
    d = 0
    for n1, g1 in enumerate(galaxies):
        for n2, g2 in enumerate(galaxies):
            if n2 > n1:
                d += dist(g1, g2)
    return d


def main():
    with open("data/day11.csv", "r") as file:
        data = file.read().splitlines()

    galaxies = parse_grid(data)
    print(list(galaxies))
    galaxies = expand_universe(galaxies, factor=1)

    answer_a = cumul_distances(galaxies)
    print(answer_a)

    galaxies_b = expand_universe(galaxies, factor=1000000)

    answer_b = cumul_distances(galaxies)
    print(answer_b)


if __name__ == "__main__":
    main()
