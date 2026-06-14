from pygad import pygad

servers = {
    0: {'cpu': 8, 'ram': 16, 'bw': 10, 'cost': 5},
    1: {'cpu': 12, 'ram': 8, 'bw': 5, 'cost': 7},
    2: {'cpu': 6, 'ram': 12, 'bw': 8, 'cost': 4}
}

N = int(input())
apps = []
for _ in range(N):
    cpu, ram, bw, profit = map(int, input().split())
    apps.append({'cpu': cpu, 'ram': ram, 'bw': bw, 'profit': profit})

def fitness_func(ga, solution, idx):
    # Treba da ja sledime potrsosuvackata za sekoj servers
    server_usage = {
        s_id: {'cpu': 0, 'ram': 0, 'bw': 0, 'profit': 0, 'active': False}
        for s_id in servers.keys()
    }

    for app_idx, server_idx in enumerate(solution):
        server_id = int(server_idx)
        app = apps[app_idx]

        # Resursite na appot gi stavme vo serverot
        server_usage[server_id]['cpu'] += app['cpu']
        server_usage[server_id]['ram'] += app['ram']
        server_usage[server_id]['bw'] += app['bw']
        server_usage[server_id]['profit'] += app['profit']
        server_usage[server_id]['active'] = True

    total_fitness = 0.0
    for s_id, usage in server_usage.items():
        if usage['active']:
            cap = servers[s_id]

            cpu_ratio = usage['cpu'] / cap['cpu']
            ram_ratio = usage['ram'] / cap['ram']
            bw_ratio = usage['bw'] / cap['bw']

            load_ratio = max(cpu_ratio, ram_ratio, bw_ratio)

            if load_ratio > 1.0:
                throughput = 1 / load_ratio
            else:
                throughput = 1.0

            server_cont = (usage['profit'] * throughput) - cap['cost']
            total_fitness += server_cont
    return total_fitness
params = {
    'num_generations': 300,
    'sol_per_pop': 50,
    'num_parents_mating': 20,
    'num_genes': N,  # TODO: fill empty params
    'gene_space': list(servers.keys()),
    'fitness_func': fitness_func,
    'mutation_num_genes': 1,
}

ga = pygad.GA(**params)
ga.run()

best_solution, _, _ = ga.best_solution(ga.last_generation_fitness)
best_fitness = fitness_func(ga, best_solution, 0)

print(f'{best_fitness:.2f}')