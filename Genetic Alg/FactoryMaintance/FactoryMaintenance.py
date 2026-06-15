import pygad
import numpy as np

machines = []
N = 0

def read_input():
    global N, machines

    N = int(input())
    for _ in range(N):
        parts = input().split()

        time = int(parts[0])
        type = parts[1]

        machines.append({'time': time, 'type': type})

def fitness_func(ga_instance, solution, solution_idx):
    global machines, N

    num_teams = N // 4

    team_sizes = []

    for i in range(num_teams):
        count = 0
        for assignment in solution:
            if assignment == i:
                count += 1
        team_sizes.append(count)

    size_penalty = sum(abs(size - 4) for size in team_sizes) * 10000

    uniqe_types = set(m['type'] for m in machines)
    best_total_type = float('inf')

    for P in uniqe_types:
        current_time = 0
        for i in range(num_teams):
            team_indexes = np.where(solution == i)[0]

            if len(team_indexes) == 0:
                    continue

            team_machines = [machines[idx] for idx in team_indexes]
            durations = [m['time'] for m in team_machines]
            types = [m['type'] for m in team_machines]

            if all(t == P for t in types):
                current_time += min(durations)
            else:
                current_time += max(durations)

        if current_time < best_total_type:
            best_total_type = current_time

    return - (best_total_type + size_penalty)


if __name__ == '__main__':
    read_input()

    num_teams = N // 4

    params = {
    'num_generations': 300,
    'sol_per_pop': 50,
    'num_parents_mating': 20,
    'num_genes': N,  # TODO: fill empty params
    'gene_space': list(range(num_teams)),
    'fitness_func': fitness_func,
    'mutation_num_genes': 1,
}

    ga = pygad.GA(**params)
    ga.run()

    best_solution, _, _ = ga.best_solution()

    best_solution = np.round(best_solution).astype(int)
    num_teams = N // 4
    unique_types = set(m['type'] for m in machines)

    final_best_time = float('inf')
    best_P = None
    teams = []

    for i in range(num_teams):
        teams.append(np.where(best_solution == i)[0])

    for P in unique_types:
        current_time = 0
        for team_indices in teams:
            team_machines = [machines[idx] for idx in team_indices]
            if all(m['type'] == P for m in team_machines):
                current_time += min(m['time'] for m in team_machines)
            else:
                current_time += max(m['time'] for m in team_machines)

        if current_time < final_best_time:
            final_best_time = current_time
            best_P = P

# Final Output Formatting
    print(final_best_time)
    print(best_P)
    for team_indices in teams:
        team_str = " ".join([f"{machines[idx]['time']}{machines[idx]['type']}" for idx in team_indices])
        print(team_str)

