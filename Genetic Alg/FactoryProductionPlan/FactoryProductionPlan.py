import pygad
import random
random.seed(0)


def read_input():
    N = int(input())
    products = []
    for _ in range(N):
        profit, mA, mB, mat, setup, labor = map(int, input().split())
        products.append({'profit': profit, 'mA': mA, 'mB': mB, 'mat': mat, 'setup': setup, 'labor': labor})
    # Read resources — handle both single-line and multi-line formats
    resource_vals = []
    while len(resource_vals) < 5:
        resource_vals += list(map(int, input().split()))
    mA_max, mB_max, materials_max, storage_max, labor_max = resource_vals[:5]
    bulk_threshold = int(input())
    return N, products, mA_max, mB_max, materials_max, storage_max, labor_max, bulk_threshold


def fitness_func(ga_instance, solution, idx):
    global products, mA_max, mB_max, materials_max, storage_max, labor_max, bulk_threshold

    total_profit = 0
    used_mA = 0
    used_mB = 0
    used_mat = 0
    used_labor = 0
    used_storage = 0

    for product_idx, quantity in enumerate(solution):
        quantity = int(quantity)

        if quantity == 0:
            continue

        prod = products[product_idx]

        used_mA      += quantity * prod['mA']
        used_mB      += quantity * prod['mB']
        used_mat     += quantity * prod['mat']
        used_labor   += quantity * prod['labor']
        used_storage += quantity

        profit_multiplier = 1.25 if quantity >= bulk_threshold else 1.0

        total_profit += (quantity * prod['profit'] * profit_multiplier) - prod['setup']

    # Death penalty for constraint violations
    if (used_mA > mA_max or used_mB > mB_max or
            used_mat > materials_max or used_labor > labor_max or
            used_storage > storage_max):
        return -999999

    return total_profit


if __name__ == "__main__":
    N, products, mA_max, mB_max, materials_max, storage_max, labor_max, bulk_threshold = read_input()

    params = {
        'num_generations': 300,
        'sol_per_pop': 50,
        'num_parents_mating': 20,
        'num_genes': N,
        'gene_space': range(16),          # each gene: integer 0..15
        'gene_type': int,                 # force integer genes
        'fitness_func': fitness_func,
        'mutation_num_genes': 1,
        'random_seed': 0,                 # reproducibility
        'keep_elitism': 2,                # keep best solutions across generations
    }

    ga = pygad.GA(**params)
    ga.run()

    best_solution, _, _ = ga.best_solution(ga.last_generation_fitness)
    best_fitness = fitness_func(ga, best_solution, 0)

    print(f'{best_fitness:.2f}')