import pygad
import random
random.seed(0)

N = int(input())
prep = []
cook = []
deadline = []
offset = []
quality = []
for _ in range(N):
    p, c, d, o, q = map(int, input().split())
    prep.append(p)
    cook.append(c)
    deadline.append(d)
    offset.append(o)
    quality.append(q)


# prep [1, 2, 1, 5, 1]
# deadline [1, 2, 1, 5, 1]
def fitness_func(ga, solution, idx):

    total_quality = 0.0
    penalty_overlap = 0.0
    early_finish_penalty = 0.0
    timings = []

    # Za sekoj gene vo genespaces
    for food_idx, start_hour in enumerate(solution):
        start_hour = int(start_hour)

        prep_time = prep[food_idx]
        cook_time = cook[food_idx]
        food_deadline = deadline[food_idx]
        food_offset = offset[food_idx]
        food_qual = quality[food_idx]

        prep_start = start_hour
        prep_end = start_hour + prep_time
        cook_start = prep_end
        cook_end = cook_start + cook_time
        finish = cook_end

        # Ako vremeto na zavrshuvanmje e pogoelmo od deadlnie
        if finish > food_deadline:
            return -999999

        # calcualte ideal - daedline - offset
        food_ideal = food_deadline - food_offset
        dev = abs(finish - food_ideal)

        dish_quality = food_qual * max(0, 1 - 0.2 * dev)
        total_quality += dish_quality

        # Malo zgolemuvanje za da preferiar tie sto zavrshile proano
        early_finish_penalty += finish * 0.0001

        # treba da gi zachuvam vo timings site tajminrana na sekoe jadenje
        timings.append((prep_start, prep_end, cook_start, cook_end))

    # Hnalding an prekplpoyuvanej
    for i in range(N):
        for j in range(i + 1, N):
            p1_start, p1_end, c1_start, c1_end = timings[i]
            p2_start, p2_end, c2_start, c2_end = timings[j]

            prep_overlap = max(0, min(p1_end, p2_end) - max(p1_start, p2_start))
            penalty_overlap -= prep_overlap * 1000

            cook_overlap = max(0, min(c1_end, c2_end) - max(c1_start, c2_start))
            penalty_overlap -= cook_overlap * 1000


    # tie braker - ako dve imaat ist total_quality togash toj so se gotvoi porano
    fitness = total_quality + penalty_overlap - early_finish_penalty
    return fitness


params = {
    'num_generations': 200,
    'sol_per_pop': 50,
    'num_parents_mating': 20,
    'num_genes': N,  # TODO: fill empty params
    'gene_space': range(24),
    'fitness_func': fitness_func,
    'mutation_num_genes': 1,
}

ga = pygad.GA(**params)
ga.run()

best_solution, _, _ = ga.best_solution(ga.last_generation_fitness)
best_fitness = fitness_func(ga, best_solution, 0)

print(f'{best_fitness:.2f}')
