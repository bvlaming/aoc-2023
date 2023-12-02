from dataclasses import dataclass
from enum import Enum


@dataclass
class Round:
    nr_red: int = 0
    nr_blue: int = 0
    nr_green: int = 0

    def power(self) -> int:
        return self.nr_red * self.nr_blue * self.nr_green


@dataclass
class Game:
    id: int
    rounds: list[Round]


class Colour(Enum):
    GREEN = "green"
    RED = "red"
    BLUE = "blue"


def parse_colour(line: str) -> tuple[Colour, int]:
    count = int("".join(([c for c in line if c.isdigit()])))
    if "red" in line:
        return Colour.RED, count
    if "green" in line:
        return Colour.GREEN, count
    return Colour.BLUE, count


def parse_round(line: str) -> Round:
    entries = [parse_colour(entry) for entry in line.split(",")]
    nr_red = sum([entry[1] for entry in entries if entry[0] == Colour.RED])
    nr_green = sum([entry[1] for entry in entries if entry[0] == Colour.GREEN])
    nr_blue = sum([entry[1] for entry in entries if entry[0] == Colour.BLUE])
    return Round(nr_red=nr_red, nr_blue=nr_blue, nr_green=nr_green)


def parse_game(line: str) -> Game:
    game_str, rounds_str = line.split(":")
    game_id = int("".join([c for c in game_str if c.isdigit()]))
    rounds = [parse_round(round_str) for round_str in rounds_str.split(";")]
    return Game(game_id, rounds)


def round_is_within_threshold(round: Round, threshold: Round) -> bool:
    return (
        (round.nr_red <= threshold.nr_red)
        & (round.nr_blue <= threshold.nr_blue)
        & (round.nr_green <= threshold.nr_green)
    )


def game_is_within_threshold(game: Game, threshold: Round) -> bool:
    return all([round_is_within_threshold(round, threshold) for round in game.rounds])


def min_balls_necessary(game: Game) -> Round:
    return Round(
        nr_red=max([round.nr_red for round in game.rounds] + [0]),
        nr_green=max([round.nr_green for round in game.rounds] + [0]),
        nr_blue=max([round.nr_blue for round in game.rounds] + [0]),
    )


def main():
    with open("data/day2.csv", "r") as file:
        data = file.read().splitlines()
    THRESHOLD = Round(nr_red=12, nr_green=13, nr_blue=14)
    games = [parse_game(line) for line in data]
    valid_game_id_2a = [
        game.id for game in games if game_is_within_threshold(game, THRESHOLD)
    ]

    print(sum(valid_game_id_2a))

    min_per_round = [min_balls_necessary(game) for game in games]

    result_2b = sum([round.power() for round in min_per_round])

    print(result_2b)


if __name__ == "__main__":
    main()
