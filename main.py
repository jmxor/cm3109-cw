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


def get_random_neighbour(x_now: list[int], c_now: int, weights: list[list[int]]) -> tuple[list[int], int]:
    """Returns a random 2-change neighbour of the given ranking and its score"""
    x_new = x_now[:]
    c_new = c_now

    # swap two random adjacent participants i and i+1
    i = random.randint(0, len(x_now) - 2)
    x_new[i], x_new[i + 1] = x_now[i + 1], x_now[i]

    # calculate new score
    c_new -= weights[x_now[i + 1]][x_now[i]]
    c_new += weights[x_new[i + 1]][x_new[i]]
    return x_new, c_new


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
        max_non_improve: int
) -> tuple[list[int], int]:
    """Return the best ranking of players using the simulated annealing
    heuristic algorithm"""

    # create initial ranking and calculate cost
    x_best = x_now = list(range(len(weights)))
    c_best = c_now = kemeny(x_now, weights)
    t = temp_initial
    num_non_improve = 0

    # loop until stopping condition met
    while 1:
        for i in range(temp_length):
            # generate random neighbour and cost
            x_new, c_new = get_random_neighbour(x_now, c_now, weights)
            delta_c = c_new - c_now

            # if energy decreased or random, move to x_new
            if delta_c <= 0 or random.random() < math.exp(-delta_c / t):
                x_now, c_now = x_new, c_new

                # update x_best, c_best
                if c_now < c_best:
                    x_best, c_best = x_now, c_now
                    num_non_improve = -1

            # stopping condition
            num_non_improve += 1
            if num_non_improve == max_non_improve:
                # print(t)
                return x_best, c_best

        t = cooling_rate * t


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
        max_non_improve=50000
    )
    end = time.perf_counter()

    # Display information
    print('Ranking:')
    for rank, index in enumerate(ranking):
        print(f'{rank+1:2} {participants[index]}')
    print(f'\nScore: {score}')
    print(f'Runtime: {(end - start) * 1000}ms')


if __name__ == '__main__':
    main()
