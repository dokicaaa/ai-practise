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

    # kreirame dictionary so verdnost od 0-10, za kolkmu kameri ima sekoja soba
    camera_counts = {i: 0 for i in range(1, 11)}
    for room in solution:
        camera_counts[int(room)] += 1

    total_security = 0.0

    # Za sekoj room
    for room_idx, info in rooms.items():
        # Zemame kolku kameri ima sekoja soba
        camera_in_room = camera_counts[room_idx]

        # Za da najdeme total security mora da nadjeme coverage an sekoja od sobite
        base_cov = 0.0

        # //Gledame dali e golema i li mala
        if room_idx in large_rooms:
            if camera_in_room == 1:
                base_cov = 0.6
            elif camera_in_room >= 2:
                base_cov = 1
        else:
            if camera_in_room >= 1:
                base_cov = 1.0

        # Sega treba da go zapazime adjecent coverage na sekoja soba
        adj_cov = 0.0
        for ajd_id in info['adjacent']:
            cams_ajdc = camera_counts[ajd_id]
            adj_cov += (cams_ajdc * 0.10)

        # mora da upotrebime min za da ne nadmineme 1.0
        total_room_coverage = min(1.0, base_cov + adj_cov)

        total_security += info['value'] * total_room_coverage

    return total_security


params = {
    'num_generations': 1000,
    'sol_per_pop': 100,
    'num_parents_mating': 40,

    'num_genes': K,
    'gene_space': list(range(1, 11)),

    'fitness_func': fitness_func,

    'mutation_num_genes': 1,
    'random_state': 0
}

ga = pygad.GA(**params)

ga.run()

best_solution, _, _ = ga.best_solution()
best_fitness = fitness_func(None, best_solution, 0)

print(f'Optimal protected value: {best_fitness}M$')
