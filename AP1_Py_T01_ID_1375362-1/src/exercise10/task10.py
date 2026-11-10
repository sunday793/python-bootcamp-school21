def solve(machines, total_time):
    seen = {}
    best = None

    for year, cost, time in machines:
        partner = (year, total_time - time)
        if partner in seen:
            total = cost + seen[partner]
            if best is None or total < best:
                best = total

        key = (year, time)
        if key not in seen or cost < seen[key]:
            seen[key] = cost

    return best


def main():
    try:
        n, total_time = map(int, input().split())
        if n <= 0 or total_time <= 0:
            print("Incorrect input")
            return
    except ValueError:
        print("Incorrect input")
        return

    machines = []

    for _ in range(n):
        try:
            year, cost, time = map(int, input().split())
            if year <= 0 or cost <= 0 or time <= 0:
                print("Incorrect input")
                return
        except ValueError:
            print("Incorrect input")
            return
        machines.append((year, cost, time))
    best = solve(machines, total_time)

    print(best)


if __name__ == "__main__":
    main()