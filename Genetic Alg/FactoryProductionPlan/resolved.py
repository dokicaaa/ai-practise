import pygad
import random
random.seed(0)


def read_input():
    # Lista od prodkuti kade sekoj item e dict od site atributi
    N = int(input())
    products = []
    for _ in range(N):
        profit, mA, mB, mat, setup, labor = map(int, input().split())
        products.append({'profit': profit, 'mA': mA, 'mB': mB, 'mat': mat, 'setup': setup, 'labor': labor})
        
    # Vnes na max tresholds za sekoj atribut
    mA_max, mB_max, materials_max, storage_max, labor_max = map(int, input().split())
    
    bulk_threshold = int(input())
    
    return N, products, mA_max, mB_max, materials_max, storage_max, labor_max, bulk_threshold


def fitness_func(ga, solution, idx):
    global N, products, mA_max, mB_max, materials_max, storage_max, labor_max, bulk_threshold
    
    # Stom se bara vkupen profit treba za sekoj gene da dodacdeme total values
    total_profit = 0
    used_mA = 0
    used_mB = 0
    used_mat = 0
    used_labor = 0
    used_storage = 0
    
    for prod_idx, quantity in enumerate(solution):
        prod_idx = int(prod_idx)
        
        # Mora prozivodot da se proizveduva
        if quantity == 0:
            continue
        
        # Go zemame od listata toj product so istito index
        prod = products[prod_idx]
        
        used_mA += quantity * prod['mA']
        used_mB += quantity * prod['mB']
        used_mat += quantity * prod['mat']
        used_labor += quantity * prod['labor']
        used_storage += quantity
        
        # total_profit ke se zgoelmuva za sekoj item vo genespace
        total_profit += (quantity * prod['profit'] * (1.25 if quantity >= bulk_threshold else 1.0) - prod['setup'])
        
        # Death peanlty - cant go over weekly max values
        if (used_mA > mA_max or used_mB > mB_max or
            used_mat > materials_max or used_labor > labor_max or
            used_storage > storage_max):
            return -999999
        
    # Treba da se optimizira, zatoa fitness value ke ni e total profit
    return total_profit

if __name__ == "__main__":
    N, products, mA_max, mB_max, materials_max, storage_max, labor_max, bulk_threshold = read_input()

    params = {
        'num_generations': 300,
        'sol_per_pop': 50,
        'num_parents_mating': 20,
        'num_genes': N,  # TODO: fill empty params
        'gene_space': range(16),
        'fitness_func': fitness_func,
        'mutation_num_genes': 1,
    }

    ga = pygad.GA(**params)
    ga.run()

    best_solution, _, _ = ga.best_solution(ga.last_generation_fitness)
    best_fitness = fitness_func(ga, best_solution, 0)

    print(f'{best_fitness:.2f}')