import pygad
import random
random.seed(0)

rooms = {
    1: {'name': 'Modern & Contemporary Art', 'adjacent': [2, 7], 'value': 110},
    2: {'name': 'European History', 'adjacent': [1, 3, 4, 5, 7], 'value': 130},
    3: {'name': 'Seasonal Exhibitions', 'adjacent': [2], 'value': 100},
    4: {'name': 'Prehistory', 'adjacent': [2, 6, 10], 'value': 140},
    5: {'name': 'Medieval Times', 'adjacent': [2, 6, 9], 'value': 120},
    6: {'name': 'Arms and Armor', 'adjacent': [4, 5], 'value': 150},
    7: {'name': 'Arts of Africa, Oceania and the Americas', 'adjacent': [1, 2, 8], 'value': 90},
    8: {'name': 'Greek and Roman History', 'adjacent': [7, 9], 'value': 180},
    9: {'name': 'The Great Hall', 'adjacent': [5, 8, 10], 'value': 30},
    10: {'name': 'Egyptian History', 'adjacent': [4, 9], 'value': 200}
}

K = int(input())

large_rooms = [2, 8, 9, 10]
def fitness_func(ga, solution, idx):
    solution = [int(x) for x in solution]
        # Death penalty e poivekoje od pokrienst od 100 procenti i ako ima povekje od K kameri

    # Kreirame dictariony od vid {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}
    counts = {i: 0 for i in range(1, 11)}
    for room in solution:
        counts[int(room)] += 1

    total_protected_value = 0.0
    for room_id, info in rooms.items():
        cams_in_room = counts[room_id]

        base_cov = 0.0
        if room_id in large_rooms:
            if cams_in_room == 1:
                base_cov = 0.6
            elif cams_in_room >= 2:
                base_cov = 1.0
        else:
            if cams_in_room >= 1:
                base_cov = 1.0

        ajd_cov = 0.0
        for adj_id in info['adjacent']:
            cams_in_adj = counts[adj_id]
            ajd_cov += (cams_in_adj * 0.10)

        total_cov = min(1.0, base_cov + ajd_cov)

        total_protected_value += info['value'] * total_cov

    return total_protected_value
params = {
    'num_generations': 1000,
    'sol_per_pop': 100,
    'num_parents_mating': 40,

    # Genot - list so golemina na 10, za sekoja ima 0, 1, 2 kameri
    # brojt na kameri vo ednas oba mozhe da e od 0 do K
    'num_genes': K,
    'gene_space': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'fitness_func': fitness_func,

    'mutation_num_genes': 1,
}
if K > 0:
    ga = pygad.GA(**params)
    ga.run()

    best_solution, _, _ = ga.best_solution()
    best_fitness = fitness_func(ga, best_solution, 0)

    print(f'Optimal protected value: {best_fitness}M$')
else:
    print('Optimal protected value: 0.0M$')