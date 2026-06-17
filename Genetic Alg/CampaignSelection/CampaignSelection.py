import pygad
import random
random.seed(0)


def read_input():
    N = int(input())
    B = int(input())
    campaigns = []
    for i in range(N):
        cost, profit, channel = input().split()
        campaigns.append({'cost': int(cost), 'profit': int(profit), 'channel': channel})
    return N, B, campaigns


def total_profit(solution):
    ...  # TODO: implement total_profit


def fitness_func(ga, solution, solution_idx):
    total = ...  # TODO: check budget, call total_profit
    return total


if __name__ == "__main__":
    N, B, campaigns = read_input()

    params = {
        'num_generations': 500,
        'sol_per_pop': 100,
        'num_parents_mating': 40,
        'num_genes': ...,  # TODO
        'gene_space': ...,  # TODO
        'fitness_func': fitness_func,
        'mutation_num_genes': 1,
    }

    ga = pygad.GA(**params)
    ga.run()

    best_solution, _, _ = ga.best_solution(ga.last_generation_fitness)

    ...  # TODO: print total cost, total profit, selected campaigns
