import pygad
import random
random.seed(0)


def read_input():
    M, N, K, D = map(int, input().split())
    B = int(input())
    blocked = set()
    for _ in range(B):
        r, c = map(int, input().split())
        blocked.add((r, c))
    return M, N, K, D, blocked


def fitness_func(ga_instance, solution, solution_idx):
    global M, N, D, blocked

    covered = set()
    used_benches = 0

    for gene in solution:
        if gene != -1:
            used_benches += 1
            r = gene // N
            c = gene % N

            if (r, c) in blocked:
                continue

            for dr in range(-D, D + 1):
                for dc in range(-D, D + 1):
                    if abs(dr) + abs(dc) <= D:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < M and 0 <= nc < N and (nr, nc) not in blocked:
                            covered.add((nr, nc))

    score = len(covered)
    penalty = used_benches * 0.5
    return score - penalty


if __name__ == "__main__":
    M, N, K, D, blocked = read_input()

    gene_space = [-1]
    for r in range(M):
        for c in range(N):
            if (r, c) not in blocked:
                gene_space.append(r * N + c)

    params = {
        'num_generations': 150,
        'sol_per_pop': 50,
        'num_parents_mating': 20,
        'num_genes': K,
        'gene_space': gene_space,
        'fitness_func': fitness_func,
        'mutation_num_genes': 1
    }

    ga = pygad.GA(**params)
    ga.run()

    best_solution, _, _ = ga.best_solution()
    best_solution = [int(x) for x in best_solution]

    covered = set()
    active_benches = []

    for gene in best_solution:
        if gene != -1:
            r = gene // N
            c = gene % N
            if (r, c) in blocked:
                continue
            active_benches.append((r, c))
            for dr in range(-D, D + 1):
                for dc in range(-D, D + 1):
                    if abs(dr) + abs(dc) <= D:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < M and 0 <= nc < N and (nr, nc) not in blocked:
                            covered.add((nr, nc))

    print(len(covered))
    print(len(active_benches))
    for r, c in active_benches:
        print(f"Bench at ({r}, {c})")
