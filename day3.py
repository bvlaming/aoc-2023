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

@dataclass
class Point:
    x: int
    y: int
    value: str
    begin_x: int | None = None
    total_val: int = 0

    def is_int(self):
        return all([c.isdigit() for c in self.value])

    def is_char(self):
        return not(self.is_int()) & (not self.value == '.')



def parse_grid(lines: list[str]) -> tuple[list[Point], int, int]:
    points = []
    max_y = len(lines)
    max_x = 0
    for x, line in enumerate(lines, start=1):
        max_x = len(line)
        for y, value in enumerate(line, start=1):
            points += Point(x, y, value)
    return points, max_x, max_y

def score_char(point: Point, points: list[Point], max_x: int, max_y: int) -> int:
    score_points = [
        int(p.value) for p in points if (
            p.is_int() and p.x >= 1 and p.y >= 1 and p.x <= max_x and p.y <= max_y
             and (abs((p.x - point.x)*(p.y - point.y)) == 1
                  or abs(p.x - point.x) + abs(p.y - point.y) == 1)
        )
    ]
    return sum(score_points)

def main():
    with open("data/day3test.csv", "r") as file:
        data = file.read().splitlines()
    points, max_x, max_y = parse_grid(data)
    special_points = [p for p in points if p.is_char()]
    scores = [p for p in points if p.is_int()]
    for x in range(1, max_x):
        begin_score_points_x = [p for p in scores if p.x == x and (
            p.y == 1 or (not any([q for q in scores if q.x == x and q.y == (p.y -1)]))
        )]
        for score_point in begin_score_points_x:
            score = score_point.value
            y_val = score_point.y
            neighbour = [p for p in points if p.x == x and p.y == y_val + 1]
            if neighbour:
                score = score * 10 + neighbour[0].value








if __name__ == "__main__":
    main()
