import pygad
import numpy as np
import random
random.seed(0)


def read_input():
    N, K = map(int, input().split())
    difficulties = [int(input()) for _ in range(N)]
    M = int(input())
    adjacencies = [tuple(map(int, input().split())) for _ in range(M)]
    return N, K, difficulties, adjacencies


def fitness_func(ga_instance, solution, solution_idx):
    #SOLUTIOPN + [2, 3, 5, 1, 2, 3] - kade inedexot na sekoj item vo nizta ni se consturciotn ID dodkea vrednosta e teamID

    time_teams = [0] * K
    team_site_counts = [0] * K
    peanlty = 0

    for site_id, team_id in enumerate(solution):
        team_id = int(team_id)
        time_teams[team_id] += difficulties[site_id]
        team_site_counts[team_id] += 1

    # Ako treba da se minimizara davbash negativna vrednost i returnuvash na kraj - od negativnata
    for count in team_site_counts:
        if count < 2:
            return -999999999

    sum_cordinated_waste = 0
    for c1, c2 in adjacencies:
        if solution[c1] != solution[c2]:
            sum_cordinated_waste += difficulties[c1] + difficulties[c2]

    max_team_time = max(time_teams)

    total_waste = max_team_time + sum_cordinated_waste
    return -total_waste

if __name__ == "__main__":
    N, K, difficulties, adjacencies = read_input()

    params = {
        'num_generations': 200,
        'sol_per_pop': 50,
        'num_parents_mating': 20,
        'num_genes': N,
        'gene_space': list(range(K)),
        'fitness_func': fitness_func,
        'mutation_num_genes': 1
    }

    ga = pygad.GA(**params)
    ga.run()

    best_solution, best_solution_fitness, _ = ga.best_solution()
    print(int(-best_solution_fitness))
    for site_id, team_id in enumerate(best_solution):
        print(f"Site {site_id} -> Team {int(team_id)}")

