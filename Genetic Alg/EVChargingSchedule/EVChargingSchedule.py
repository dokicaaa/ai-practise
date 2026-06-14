import pygad
import random
import math
random.seed(0)

charger_power = 10
grid_capacity = 40
solar = [0, 0, 0, 0, 0, 0, 0, 3, 7, 12, 15, 16, 16, 15, 12, 7, 3, 0, 0, 0, 0, 0, 0, 0]
price = [0.15] * 24
for h in [8, 9, 10, 11, 17, 18, 19, 20]:
    price[h] = 0.30

N = int(input())
kwh = []
arrival_hour = []
departure_hour = []
for _ in range(N):
    k, a, d = map(int, input().split())
    kwh.append(k)
    arrival_hour.append(a)
    departure_hour.append(d)

hours_needed = [math.ceil(k / charger_power) for k in kwh]


def fitness_func(ga, solution, idx):
    ...  # TODO: implement fitness function


params = {
    'num_generations': 200,
    'sol_per_pop': 50,
    'num_parents_mating': 20,
    'num_genes': ...,  # TODO: fill empty params
    'gene_space': ...,
    'fitness_func': fitness_func,
    'mutation_num_genes': 1,
}

ga = pygad.GA(**params)
ga.run()

best_solution, _, _ = ga.best_solution(ga.last_generation_fitness)
best_fitness = fitness_func(ga, best_solution, 0)

print(f'{-best_fitness:.2f}')