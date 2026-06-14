import pygad
import math

N, M, R = map(float, input().split())
N = int(N)
M = int(M)
points = [tuple(map(float, input().split())) for _ in range(N)]

if points:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x_min, x_max = min(xs) - R, max(xs) + R
    y_min, y_max = min(ys) - R, max(ys) + R
else:
    x_min, x_max, y_min, y_max = 0, 10, 0, 10


def decode(solution):
    centers = []
    for i in range(len(solution) // 2):
        x = solution[2 * i]
        y = solution[2 * i + 1]
        if x > -100 and y > -100:
            centers.append((x, y))
    return centers


def fitness_func(ga, solution, idx):
    centers = decode(solution)
    num_umbrellas = len(centers)

    uncovered = 0
    small_overlap = 0
    large_overlap = 0

    for px, py in points:
        count = 0
        for cx, cy in centers:
            dist = math.sqrt((px - cx) ** 2 + (py - cy) ** 2)
            if dist <= R:
                count += 1
        if count == 0:
            uncovered += 1
        elif count == 2:
            small_overlap += 1
        elif count >= 3:
            large_overlap += (count - 1)

    penalty = (
        10000 * uncovered
        + 100 * large_overlap
        + 10 * small_overlap
        + 1 * num_umbrellas
    )

    return -penalty


gene_space = []
for i in range(M):
    gene_space.append({'low': x_min, 'high': x_max})
    gene_space.append({'low': y_min, 'high': y_max})

params = {
    'num_generations': 500,
    'sol_per_pop': 100,
    'num_parents_mating': 50,
    'num_genes': 2 * M,
    'gene_space': gene_space,
    'fitness_func': fitness_func,
    'mutation_num_genes': 1,
    'save_best_solutions': True
}
ga = pygad.GA(**params)
ga.run()
solution, _, _ = ga.best_solution()
fitness = fitness_func(None, solution, 0)
best_solutions = ga.best_solutions
print(solution)
print(fitness)

c1 = [10.0, 10.0, 10.0, 10.0, 10.0, 10.0]
c2 = [5.0, 5.0, 10.0, 10.0, 10.0, 10.0]
c3 = [1.0, 1.0, 1.1, 1.0, 5.0, 5.0]
c4 = [1.05, 1.0, 5.0, 5.0, 10.0, 10.0]
c5 = [1.05, 1.0, 5.0, 5.0, -0.5, -0.5]

chromosomes = [c1, c2, c3, c4, c5]

submit_data(fitness_func, decode, chromosomes, best_solutions)