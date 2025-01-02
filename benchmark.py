import matplotlib.pyplot as plt
import time
import sys

from main import *


def benchmark_non_improve():
    times = []
    scores = []
    tournament_file = sys.argv[1]
    participants, tournament = load_tournament(tournament_file)
    n_values = range(1)
    for n in n_values:
        print(n)
        temp_times = []
        temp_scores = []
        for i in range(100):
            start = time.perf_counter()
            ranking, score = solve_simulated_annealing(tournament, 1, 2000, 0.99, 50000)
            end = time.perf_counter()
            temp_scores.append(score)
            temp_times.append(end - start)
        scores.append(sum(temp_scores) / len(temp_scores))
        times.append(sum(temp_times) / len(temp_times))

    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('a')
    ax1.set_ylabel('avg. score', color=color)
    ax1.plot(list(map(lambda x: x/100, list(n_values))), scores, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:red'
    ax2.set_ylabel('avg. runtime', color=color)  # we already handled the x-label with ax1
    ax2.plot(list(map(lambda x: x/100, list(n_values))), times, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

    print(scores[0])
    print(times[0])


def main():
    benchmark_non_improve()


if __name__ == '__main__':
    main()
