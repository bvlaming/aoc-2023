def distance_reached(holding_time: int, max_time: int):
    if holding_time >= max_time:
        return 0
    elif holding_time == 0:
        return 0
    speed = holding_time
    return (max_time - holding_time) * holding_time


def allowed_holding_times(time: int, distance: int):
    ct = 0
    for ht in range(0, time):
        if distance_reached(ht, time) > distance:
            ct += 1
    return ct


def main():
    times = [50, 74, 86, 85]
    distances = [242, 1017, 1691, 1252]

    answer_a = (
        allowed_holding_times(50, 242)
        * allowed_holding_times(74, 1017)
        * allowed_holding_times(86, 1691)
        * allowed_holding_times(85, 1252)
    )
    print(answer_a)

    print(allowed_holding_times(50748685, 242101716911252))


if __name__ == "__main__":
    main()
