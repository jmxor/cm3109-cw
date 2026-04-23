import argparse
import itertools
import math
import random
import time


def load_tournament(filename: str) -> tuple[list[str], list[list[int]]]:
    with open(filename) as file:
        # load number of participants
        n = int(file.readline())

        # load participants
        participants = []
        for i in range(n):
            index, name = file.readline().strip().split(",")
            participants.append(name)

        # skip line
        file.readline()

        # load tournament weightings
        tournament = [[0 for i in range(n)] for j in range(n)]
        while True:
            line = file.readline()
            if not line:
                break

            w, p1, p2 = line.split(",")
            tournament[int(p1) - 1][int(p2) - 1] = int(w)

    return participants, tournament


def kemeny(ranking: list[int], weights: list[list[int]]) -> int:
    """Return the kemeny score of a ranking given weights"""
    # ranking order is preserved so p1 always has a better rank than p2
    c = 0
    for p1, p2 in itertools.combinations(ranking, 2):
        c += weights[p2][p1]
    return c


def solve_simulated_annealing(
    weights: list[list[int]],
    temp_initial: float,
    temp_length: int,
    cooling_rate: float,
    max_non_improve: int,
) -> tuple[list[int], int]:
    """Return the best ranking of players using the simulated annealing
    heuristic algorithm"""

    # create initial ranking and calculate cost
    n = len(weights)
    x_best = list(range(n))
    x_now = x_best.copy()
    c_now = kemeny(x_now, weights)
    c_best = c_now
    t = temp_initial
    num_non_improve = 0

    # loop until stopping condition met
    while num_non_improve < max_non_improve:
        for _ in range(temp_length):
            # Generate a random neighbouring ranking by swapping two adjacent
            # elements and calculate the change in cost.
            i = random.randint(0, n - 2)
            a = x_now[i]
            b = x_now[i + 1]
            c_delta = weights[a][b] - weights[b][a]

            # If the cost change is < 0 or random, move to new ranking
            if c_delta <= 0 or random.random() < math.exp(-c_delta / t):
                x_now[i], x_now[i + 1] = b, a
                c_now += c_delta

                # update x_best, c_best
                if c_now < c_best:
                    x_best = x_now.copy()
                    c_best = c_now
                    num_non_improve = -1

            # stopping condition
            num_non_improve += 1
            if num_non_improve == max_non_improve:
                break

        t = cooling_rate * t

    return x_best, c_best


def main():
    # Load tournament
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()
    try:
        participants, tournament = load_tournament(args.file)
    except FileNotFoundError:
        print(f'Error: file "{args.file}" could not be loaded')
        return

    # Solve tournament
    start = time.perf_counter()
    ranking, score = solve_simulated_annealing(
        weights=tournament,
        temp_initial=1,
        temp_length=2000,
        cooling_rate=0.99,
        max_non_improve=50000,
    )
    end = time.perf_counter()

    # Display information
    print("Ranking:")
    for rank, index in enumerate(ranking):
        print(f"{rank + 1:2} {participants[index]}")
    print(f"\nScore: {score}")
    print(f"Runtime: {(end - start) * 1000}ms")


if __name__ == "__main__":
    main()
