import pygad
import random
random.seed(0)

solar = [0, 0, 0, 0, 0, 0, 0, 500, 1200, 2000, 2700, 3000, 3000, 2700, 2000, 1200, 500, 0, 0, 0, 0, 0, 0, 0]
price = [0.15] * 24
for h in [8, 9, 10, 11, 17, 18, 19, 20]:
    price[h] = 0.30
GRID_LIMIT = 5000

N = int(input())
appliances = []
for _ in range(N):
    watts, runtime, earliest, latest, priority = map(int, input().split())
    appliances.append({'watts': watts, 'runtime': runtime, 'earliest': earliest, 'latest': latest})


def fitness_func(ga, solution, idx):
    hourly_demand = [0] * 24


    for app_idx, start_hour in enumerate(solution):
        start_hour = int(start_hour)

        app_info = appliances[app_idx]

        # Ako start hour e pred rangeot togash e penalty
        if start_hour < app_info['earliest']:
            return -9999999

        end_hour = start_hour + app_info['runtime']
        if end_hour > app_info['latest']:
            return -9999999

        for h in range(start_hour, end_hour):
            if h >= 24:
                return -9999999

            hourly_demand[h] += app_info['watts']

    # Siimulacija za sekoj chas od denot
    total_cost = 0.0
    for h in range(24):
        # DEATH PENALTY
        if hourly_demand[h] > GRID_LIMIT:
            return -9999999

        net = max(0, hourly_demand[h] - solar[h])
        total_cost += net / 1000 * price[h]

    return -total_cost

params = {
    'num_generations': 200,
    'sol_per_pop': 50,
    'num_parents_mating': 20,
    'num_genes': N,
    'gene_space': range(24),
    'fitness_func': fitness_func,
    'mutation_num_genes': 1,
}

ga = pygad.GA(**params)
ga.run()

best_solution, _, _ = ga.best_solution(ga.last_generation_fitness)
best_fitness = fitness_func(ga, best_solution, 0)

print(f'{-best_fitness:.2f}')