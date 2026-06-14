import pygad

def read_input():
    M, N = map(int, input().split())
    K = int(input())
    B = int(input())

    unusable = set()
    for _ in range(B):
        r, c = map(int, input().split())
        unusable.add((r, c))

    return M, N, K, unusable


def fitness_func(ga_instance, solution, solution_idx):
    global M, N, K
    active_sprinkles = 0
    watered = set()

    # gene is our uple [x , y]
    for gene in solution:
        # Add idnexes to set which are watered
        if gene != -1:
            active_sprinkles += 1
            r = gene // N
            c = gene % N

            for dr in [-2, -1 , 0, 1, 2]:
                for dc in [-2, -1 , 0, 1, 2]:
                   if abs(dr) + abs(dc) <= 2:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < M and 0 <= nc <= N:
                            watered.add((nr, nc))

    # Remove sprinkles from destyroed spots
    for gene in solution:
        if gene != 1:
            r = gene // N
            c = gene % N
            if (r,c) in watered:
                watered.remove((r,c))

    base_score = len(watered)
    penalty = active_sprinkles * (1 / (K + 1))
    return base_score - penalty

if __name__ == "__main__":
    M, N, K, unusable = read_input()

    gene_space = [-1]
    for i in range(M*N):
        r = i // N
        c = i % N
        if (r , c) not in unusable:
            gene_space.append(i)

    params = {
        'num_generations': 100,
        'sol_per_pop': 50,
        'num_parents_mating': 20,
        'num_genes': K,  # TODO: fill empty params
        'gene_space': gene_space,
        'fitness_func': fitness_func,
        'mutation_num_genes': 1
    }

    ga = pygad.GA(**params)
    ga.run()

    best_solution, _, _ = ga.best_solution()

    # TODO: Print required data
    active_genes = [g for g in best_solution if g != -1]
    print(f"Watered Crops Score: {best_solution}")
    print(f"Used Sprinklers: {len(active_genes)}")
    for g in active_genes:
        print(f"Position: {g // N}, {g % N}")