from dataclasses import dataclass

MAPS = {
    "ftw": "data/day5-fertilizertowater.csv",
    "htl": "data/day5-humiditytolocation.csv",
    "ltt": "data/day5-lighttotemperature.csv",
    "sts": "data/day5-seedtosoil.csv",
    "stf": "data/day5-soiltofertilizer.csv",
    "tth": "data/day5-temperaturetohumidity.csv",
    "wtl": "data/day5-watertolight.csv",
}

MAPS_TEST = {
    "ftw": "data/day5-test-fertilizertowater.csv",
    "htl": "data/day5-test-humiditytolocation.csv",
    "ltt": "data/day5-test-lighttotemperature.csv",
    "sts": "data/day5-test-seedtosoil.csv",
    "stf": "data/day5-test-soiltofertilizer.csv",
    "tth": "data/day5-test-temperaturetohumidity.csv",
    "wtl": "data/day5-test-watertolight.csv",
}


@dataclass
class DictRow:
    x_i: int
    y_i: int
    delta: int


class BasMap:
    def __init__(self, dictrows: list[DictRow]):
        self.dictrows = dictrows
        self.change_points = {dictrow.x_i for dictrow in self.dictrows}.union(
            {dictrow.x_i + dictrow.delta - 1 for dictrow in self.dictrows}
        )

    def get(self, key: int) -> int:
        for dictrow in self.dictrows:
            if key >= dictrow.x_i and key < (dictrow.x_i + dictrow.delta):
                return dictrow.y_i + key - dictrow.x_i
        return key


def get_values(
    seed_ranges: list[tuple[int, int]], mapping: BasMap
) -> list[tuple[int, int]]:
    def update_seed_ranges(seed_ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
        new_sr = []
        for sr in seed_ranges:
            points_in_sr = [p for p in mapping.change_points if sr[0] <= p < sr[1]]
            points_in_sr.sort()
            if len(points_in_sr) == 0:
                new_sr += [sr]
            else:
                all_points = [sr[0]] + points_in_sr + [sr[1]]
                for n, p in enumerate(all_points):
                    if n < len(all_points) - 1:
                        new_sr += [(all_points[n], all_points[n + 1] - 1)]
        return new_sr

    new_ranges = update_seed_ranges(seed_ranges)
    print(len(new_ranges))
    return [(mapping.get(range[0]), mapping.get(range[1])) for range in new_ranges]


def get_value(seed: int, mapping: BasMap):
    return mapping.get(seed)


def parse_map(path: str) -> BasMap:
    """files contain source start, target start, range length."""
    with open(path, "r") as file:
        data = file.read().splitlines()
    dictrows = [
        DictRow(int(line.split()[1]), int(line.split()[0]), int(line.split()[2]))
        for line in data
    ]
    return BasMap(dictrows)


def find_locations(
    seed_ranges: list[tuple[int, int]], maps: dict[str, BasMap]
) -> list[tuple[int, int]]:
    x = seed_ranges
    for k in ["sts", "stf", "ftw", "wtl", "ltt", "tth", "htl"]:
        x = get_values(x, maps[k])
    return x


def find_location(seed: int, maps: dict[str, BasMap]) -> int:
    "seed - soil - fert - water - light - temp - humid - loc"
    x = seed
    for k in ["sts", "stf", "ftw", "wtl", "ltt", "tth", "htl"]:
        x = get_value(x, maps[k])
    return x


def main():
    with open("data/day5-seeds.csv", "r") as file:
        seeds_data = file.read()

    seeds = [int(seed) for seed in seeds_data.split()]

    maps = {id: parse_map(path) for id, path in MAPS.items()}

    locations = [find_location(seed, maps) for seed in seeds]

    print(f"answer a: {min(locations)}")
    # b.
    seed_ranges = [
        (seeds[2 * n], seeds[2 * n] + seeds[2 * n + 1]) for n in range(len(seeds) // 2)
    ]

    location_ranges = find_locations(seed_ranges, maps)

    answer_b = min(min(x[0], x[1]) for x in location_ranges)
    print(f"answer b: {answer_b}")


if __name__ == "__main__":
    main()
