from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int
    value: str

    def __hash__(self):
        return hash((self.x, self.y))


def parse_grid(lines: list[str]) -> list[Point]:
    points = []
    for y, line in enumerate(lines, start=1):
        for x, value in enumerate(line, start=1):
            points += [Point(x, y, value)]
    return points


def parse_dict(
    grid: list[Point], point_dict: dict[tuple[int, int], Point]
) -> tuple[dict[Point, tuple[Point, Point]], Point]:
    """Return the dict connecting points, and the starting point.

    Note that in this convention, y increases N to S and x increases W to E.
    """
    path_dict = {}
    for p in grid:
        # skip over . ; also S is a special case. All others: connect to its neighbours
        if p.value != ".":
            # if it doesn't connect to a parseable neighbour, it's not part of the path.
            try:
                if p.value == "|":
                    path_dict[p] = (
                        point_dict[(p.x, p.y - 1)],
                        point_dict[(p.x, p.y + 1)],
                    )
                if p.value == "-":
                    path_dict[p] = (
                        point_dict[(p.x - 1, p.y)],
                        point_dict[(p.x + 1, p.y)],
                    )
                if p.value == "J":
                    path_dict[p] = (
                        point_dict[(p.x - 1, p.y)],
                        point_dict[(p.x, p.y - 1)],
                    )
                if p.value == "L":
                    path_dict[p] = (
                        point_dict[(p.x + 1, p.y)],
                        point_dict[(p.x, p.y - 1)],
                    )
                if p.value == "7":
                    path_dict[p] = (
                        point_dict[(p.x - 1, p.y)],
                        point_dict[(p.x, p.y + 1)],
                    )
                if p.value == "F":
                    path_dict[p] = (
                        point_dict[(p.x + 1, p.y)],
                        point_dict[(p.x, p.y + 1)],
                    )
            except KeyError:
                pass
    starting_point = [p for p in grid if p.value == "S"][0]
    return path_dict, starting_point


def track_path(
    path_dict: dict[Point, tuple[Point, Point]], start: Point
) -> list[Point]:
    next_to_start = [
        k for k, v in path_dict.items() if (v[0] == start or v[1] == start)
    ]
    current_point = next_to_start[0]
    path = [current_point]
    back_at_start = False
    prev_point = start
    while not back_at_start:
        connecting_point = [p for p in path_dict[current_point] if p != prev_point][0]
        path += [connecting_point]
        if connecting_point == start:
            back_at_start = True
        else:
            prev_point = current_point
            current_point = connecting_point
    return path


def count_area(
    points: list[Point], path: list[Point], point_dict: dict[tuple[int, int], Point]
) -> int:
    """For every point, decrease y until we get to zero. Count the number of
    crossings the path. Crossing the path means crossing either -, or {F, J} or {7, L}
    """
    non_path = [p for p in points if p not in path]
    # S -> L in the data
    s_replacement = "L"
    inside = 0
    for p in non_path:
        crossings = 0
        entry_point: Point | None = None
        current_point = p
        while current_point.y > 1:
            next_point = point_dict[(current_point.x, current_point.y - 1)]
            if next_point in path and next_point.value != "|":
                if next_point.value == "S":
                    next_point.value = s_replacement
                if next_point.value == "-":
                    crossings += 1
                else:
                    if not entry_point:
                        entry_point = next_point
                    else:
                        entry_exit = {entry_point.value, next_point.value}
                        if entry_exit == {"J", "F"} or entry_exit == {"7", "L"}:
                            crossings += 1
                        entry_point = None
            current_point = next_point
        if crossings % 2 == 1:
            inside += 1
    return inside


def main():
    with open("data/day10.csv", "r") as file:
        data = file.read().splitlines()

    points = parse_grid(data)
    point_dict = {(p.x, p.y): p for p in points}
    path_dict, start = parse_dict(points, point_dict)
    print(start)
    # start not at S, but at a point connecting to S. Then, go in the other direction,
    # check when we get to S.
    path_followed = track_path(path_dict, start)
    print(len(path_followed) // 2)

    # to calculate the area: for every point, move towards the edge. anything outside
    # will cross the path zero or an even amount of times; anything inside will cross
    # the path an odd number of times.
    area = count_area(points, path_followed, point_dict)
    print(area)


if __name__ == "__main__":
    main()
