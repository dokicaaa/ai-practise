import pygad
from sklearn.tree import DecisionTreeClassifier

dataset = [
    [2, 3, 1, 7, 0],
    [5, 6, 4, 3, 1],
    [1, 1, 2, 8, 1],
    [7, 8, 6, 4, 1],
    [3, 2, 1, 9, 0],
    [8, 7, 5, 2, 1],
    [4, 5, 2, 6, 1],
    [1, 3, 1, 9, 0],
    [9, 8, 7, 2, 1],
    [2, 2, 3, 8, 0]
]

...  # TODO: Split dataset here


def fitness_func(ga_instance, solution, solution_idx):
    ...  # TODO: Define fitness function


ga_instance = pygad.GA(
    num_generations=40,
    sol_per_pop=50,
    num_parents_mating=25,
    fitness_func=fitness_func,
    num_genes=...,  # TODO: Define missing params
    gene_space=...,
    mutation_num_genes=1
)

ga_instance.run()
best_solution, _, _ = ga_instance.best_solution()

...  # TODO: Print best params and accuracy of best model