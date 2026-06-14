import pygad
import numpy as np
import random
random.seed(0)


def read_input():
    N, K = map(int, input().split())
    times = [int(input()) for _ in range(N)]
    speeds = [float(input()) for _ in range(K)]
    return N, K, times, speeds


def fitness_func(ga_instance, solution, solution_idx):
    # solution - [2,1,2,4,1] - index ke ni e task_id dodeka balue ke ni e machine_id

    machine_times = [0.0] * K
    for task_id, machine_id in enumerate(solution):
        machine_id = int(machine_id)

        task_time = times[task_id]
        machine_speed = speeds[machine_id]

        actual_time = task_time/ machine_speed

        machine_times[machine_id] += actual_time

    makespan = max(machine_times)

    return -makespan



if __name__ == "__main__":
    N, K, times, speeds = read_input()

    params = {
        'num_generations': 200,
        'sol_per_pop': 50,
        'num_parents_mating': 20,
        'num_genes': N,
        'gene_space': list(range(K)),
        'fitness_func': fitness_func,
        'mutation_num_genes': 1
    }

    ga = pygad.GA(**params)
    ga.run()
    best_solution, best_solution_fitness, _ = ga.best_solution()

    # Фитнесот е негативниот makespan, па го множиме со -1
    best_makespan = -best_solution_fitness

    # Печатење на makespan заокружен на 1 децимала
    print(f"{best_makespan:.1f}")

    # Печатење на распоредот по машини
    best_solution = np.round(best_solution).astype(int)
    assigned_tasks = []
    for current_machine in range(K):
        assigned_tasks = []

        # Сега изминуваме низ решението за да ги најдеме задачите за оваа машина
        for task_id, machine_id in enumerate(best_solution):
            if machine_id == current_machine:
                assigned_tasks.append(str(task_id))

        # Печатиме откако ќе ги собереме сите задачи за тековната машина
        print(f"Machine {current_machine}: {' '.join(assigned_tasks)}")