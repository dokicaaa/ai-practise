import pygad
import random
random.seed(0)

solar = [0, 0, 0, 0, 0, 0, 0, 500, 1200, 2000, 2700, 3000, 3000, 2700, 2000, 1200, 500, 0, 0, 0, 0, 0, 0, 0]
price = [0.15] * 24
for h in [8, 9, 10, 11, 17, 18, 19, 20]:
    price[h] = 0.30
GRID_LIMIT = 5000


N = int(input())
appliances = []
for _ in range(N):
    watts, runtime, earliest, latest, priority = map(int, input().split())
    appliances.append({'watts': watts, 'runtime': runtime, 'earliest': earliest, 'latest': latest})


#  [[500w, 2, 12, 15,]]

def fitness_func(ga, solution, idx):
    # Niza za site saat kolku wati trsohat
    hourly_demand = [0.0] * 24
    
    for unit_id, hour in enumerate(solution):
        hour = int(hour)
        
        app_info = appliances[unit_id]
        
    # Ako start time na appliance e pred nadvor od window togash penalty
    if hour < app_info['earliest']:
        return -999999
    # Ako applince zavrshuva posle latest chas
    end_hour = hour + app_info['runtime']
    if end_hour > app_info['latest']:
        return -999999
    
    # Ne smee sekoj saat da e pogolem od 23
    for h in range(hour, end_hour):
        if h >= 24:
            return -999999
        
        hourly_demand[h] += app_info['watts']
    
    total_spend = 0.0
    # Simulacija na trsohosk
    for h in range(24):
        if hourly_demand[h] > GRID_LIMIT:
            return -999999
        
        net = max(0, hourly_demand[h] - solar[h])
        total_spend += net / 1000 * price[h]

    return -total_spend


# Bidejki treba da vidime koj ured e vo koj saat ke bide idx - ured idx i 0-23 za koj asaat e

params = {
    'num_generations': 200,
    'sol_per_pop': 50,
    'num_parents_mating': 20,
    'num_genes': N,  # TODO: fill empty params
    'gene_space': range(24),
    'fitness_func': fitness_func,
    'mutation_num_genes': 1,
}

ga = pygad.GA(**params)
ga.run()

best_solution, _, _ = ga.best_solution(ga.last_generation_fitness)
best_fitness = fitness_func(ga, best_solution, 0)

print(f'{-best_fitness:.2f}')