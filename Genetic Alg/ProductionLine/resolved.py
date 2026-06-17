import pygad
import numpy as np


def read_input():
    N, K = map(int, input().split())
    times = [int(input()) for _ in range(N)]
    speeds = [float(input()) for _ in range(K)]
    return N, K, times, speeds

# Bidejki treba da gledame kolku n zadaci se stavile na sekoja ka mashina
# Genot ke ni bide -> [2, 4, 5, 1, 5,] indeksot ke ni e N zadaca, na koja mashina bila dodela
# Za da mozhe da izborime kolku mashini se dodale za sekoja
def fitness_func(ga_instance, solution, solution_idx):
    
    # Inicijalizirame lista so 0.0 vreme za sekoja moshina
    machine_times = [0.0] * K
    for task_id, machine_id in enumerate(solution):
        machine_id = int(machine_id)
        
        speed = speeds[machine_id]
        proc_time = times[task_id]
    
        total_time = proc_time / speed
    
        machine_times[machine_id] += total_time
    
    
    makespan = max(machine_times)
    # Treba da se minimizira odnosno stavame -
    return -makespan 
    

if __name__ == "__main__":
    N, K, times, speeds = read_input()

    params = {
        'num_generations': 200,
        'sol_per_pop': 50,
        'num_parents_mating': 20,
        'num_genes': N,  # TODO: fill empty params
        'gene_space': list(range(K)),
        'fitness_func': fitness_func,
        'mutation_num_genes': 1
    }

    ga = pygad.GA(**params)
    ga.run()

    best_solution, best_solution_fitness, _ = ga.best_solution()

    ...  # TODO: Print required data
    best_makespan = -best_solution_fitness
    
    print(f"{best_makespan:.1f}")
    
    machines = {i: [] for i in range(K)}
    
    for task_id, machine_id in enumerate(best_solution):
        machine_id = int(machine_id)
        
        machines[machine_id].append(task_id)
        
    for i in range(K):
        
        tasks_str = " ".join(map(str, machines[i]))
        print(f"Machine {i}: {tasks_str}")
    
    
    