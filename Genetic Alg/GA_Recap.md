# Genetic Algorithm Patterns — Full Recap

## Quick Reference

| Problem | Encoding | Gene Meaning | Gene Space | Data Access | Sign | Death Penalty | Output |
|---------|----------|-------------|------------|-------------|------|---------------|--------|
| MuseumCameras | Selection | room ID (1..10) | `[1..10]` | `dict[key]['value']` | +max | none | `f'{v}M$'` |
| MaxCrops | Selection | cell index or -1 | `[-1, 0..M*N-1]` | `set`, scalars | +max | none | `"Position: {r}, {c}"` |
| CityPark | Selection | cell index or -1 | `[-1, 0..M*N-1]` | `set`, scalars | +max | none | `"Bench at ({r}, {c})"` |
| ConstructSites | Assignment | team ID (0..K-1) | `range(K)` | `list[]` | −min | `-999999999` | `"Site {id} -> Team {t}"` |
| ProductionLine | Assignment | machine ID (0..K-1) | `range(K)` | `list[]` | −min | none | `"Machine {m}: {tasks}"` |
| FactoryMaintenance | Assignment | team ID (0..num_teams-1) | `range(num_teams)` | `list of dicts` | −min | size penalty | custom multi-line |
| ServerLoadBalancer | Assignment | server ID (0..2) | `list(servers.keys())` | `dict[key]['cpu']` | +max | none | `f'{v:.2f}'` |
| FactoryProductionPlan | Quantity | product count (0..15) | `range(16)` | `list of dicts` | +max | `-999999` | `f'{v:.2f}'` |
| ParamOptimisation | Float | hyperparameter index | `[choices...]` | `list of lists` | +max | none | best params + acc |
| SmartHomeScheduler | Temporal | start hour (0..23) | `range(24)` | `list of dicts` | −min | `-9999999` | `f'{-v:.2f}'` |
| EVChargingSchedule | Temporal | start hour (0..23) | `range(24)` | flat `list[]` | −min | `-100000` | `f'{-v:.2f}'` |
| CookingSchedule | Temporal | start hour (0..23) | `range(24)` | flat `list[]` | +max | `-999999` | `f'{v:.2f}'` |

---

## 1. Selection / Placement Encoding

**Gene = ID of the selected item** (room number, grid cell index).  
`num_genes = K` (how many items to place).

### Pattern

```python
# MuseumCameras — gene = room_id from 1..10, K cameras to place
rooms = {1: {'adjacent': [2, 7], 'value': 110}, ...}
large_rooms = [2, 8, 9, 10]

# Count how many cameras end up in each room
counts = {i: 0 for i in range(1, 11)}
for room in solution:
    counts[int(room)] += 1

# Evaluate coverage per room
for room_id, info in rooms.items():
    cams_in_room = counts[room_id]
    if room_id in large_rooms:
        base_cov = 0.6 if cams_in_room == 1 else (1.0 if cams_in_room >= 2 else 0.0)
    else:
        base_cov = 1.0 if cams_in_room >= 1 else 0.0
    # Adjacent contribution
    for adj_id in info['adjacent']:
        base_cov += counts[adj_id] * 0.10
    total_protected += info['value'] * min(1.0, base_cov)

return total_protected
```

```python
# MaxCrops / CityPark — gene = cell index or -1 (unused sentinel)
gene_space = [-1]
for r in range(M):
    for c in range(N):
        if (r, c) not in blocked:
            gene_space.append(r * N + c)

# In fitness: -1 means "no sprinkler/bench here"
for gene in solution:
    if gene != -1:
        r = gene // N
        c = gene % N
        # ... manhattan / diamond coverage check
        covered.add((r, c))

# Tie-breaker: prefer fewer used items
score = len(covered)
penalty = used_count * 0.5   # or 1/(K+1)
return score - penalty
```

### Key points
- `-1` as sentinel for "not used"  
- `gene // N, gene % N` to decode cell index → coordinates  
- Coverage via set of unique cells (duplicates automatically handled)  

---

## 2. Integer Assignment Encoding

**Gene = group ID** (team, machine, server) that an item is assigned to.  
`num_genes = N` (items to assign).  
`gene_space = range(K)` where K = number of groups.

### Pattern

```python
# solution[i] = group_id for item i
group_totals = [0] * K    # or [0.0] * K

for item_idx, group_id in enumerate(solution):
    group_id = int(group_id)
    group_totals[group_id] += item_values[item_idx]

# Hard constraint: each team needs at least 2 items
if any(count < 2 for count in group_counts):
    return -999999999

# Objective: minimize max(group_totals) + coordination_cost
result = max(group_totals) + coordination_penalty
return -result             # negative because GA maximizes
```

### Variants

```python
# ProductionLine — machine load with different speeds
machine_times = [0.0] * K
for task_id, machine_id in enumerate(solution):
    machine_id = int(machine_id)
    machine_times[machine_id] += times[task_id] / speeds[machine_id]
makespan = max(machine_times)
return -makespan
```

```python
# ServerLoadBalancer — multi-resource packing + throttling
server_usage = {sid: {'cpu': 0, 'ram': 0, 'bw': 0, 'profit': 0} for sid in servers}
for app_idx, server_id in enumerate(solution):
    app = apps[app_idx]
    server_usage[server_id]['cpu'] += app['cpu']
    server_usage[server_id]['ram'] += app['ram']
    server_usage[server_id]['bw']  += app['bw']

for sid, usage in server_usage.items():
    cpu_r = usage['cpu'] / servers[sid]['cpu']
    ram_r = usage['ram'] / servers[sid]['ram']
    bw_r  = usage['bw']  / servers[sid]['bw']
    load  = max(cpu_r, ram_r, bw_r)
    throughput = 1.0 / load if load > 1.0 else 1.0
    total += usage['profit'] * throughput - servers[sid]['cost']
return total
```

---

## 3. Integer Quantity Encoding

**Gene = quantity** of something to produce.  
`num_genes = N` (different products).  
`gene_space = range(0, 16)` (0–15 units each).

### Pattern

```python
# FactoryProductionPlan
total_profit = 0
used = [0] * 5    # resources: mA, mB, mat, storage, labor

for idx, qty in enumerate(solution):
    qty = int(qty)
    if qty == 0:
        continue
    prod = products[idx]          # {'profit': .., 'mA': .., 'setup': ..}
    used[0] += qty * prod['mA']
    used[1] += qty * prod['mB']
    used[2] += qty * prod['mat']
    used[3] += qty                # storage = count
    used[4] += qty * prod['labor']

    mult = 1.25 if qty >= bulk_threshold else 1.0
    total_profit += qty * prod['profit'] * mult - prod['setup']

# Death penalty if any limit exceeded
if any(u > limit for u, limit in zip(used, limits)):
    return -999999

return total_profit
```

### Key points
- `gene_type=int` forces integer genes  
- Bulk discount creates non-linear profit (diminishing returns)  
- Setup cost creates threshold effect (minimum profitable qty)  

---

## 4. Continuous Float Encoding

**Gene = index into a list of candidate values.**  
Used for hyperparameter optimization.

### Pattern

```python
# ParamOptimisation
criterion_choices   = ['gini', 'entropy']
max_depth_choices   = [5, 10, 15, 20, 25]
min_samples_choices = [2, 3, 4, 5, 10]
max_leaf_choices    = [5, 10, 15, 20, 25]

# solution = [criterion_idx, depth_idx, samples_idx, leaf_idx]
criterion   = criterion_choices[int(solution[0])]
max_depth   = max_depth_choices[int(solution[1])]
min_samples = min_samples_choices[int(solution[2])]
max_leaf    = max_leaf_choices[int(solution[3])]

model = DecisionTreeClassifier(
    criterion=criterion, max_depth=max_depth,
    min_samples_split=min_samples, max_leaf_nodes=max_leaf)
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)

# Tie-breaker: prefer smaller trees
size_penalty = (max_depth + max_leaf) * 0.001
return accuracy - size_penalty
```

### Key points
- `gene_space = [criterion_choices, max_depth_choices, ...]` — each gene has its own list  
- `num_genes = 4` (fixed, one per hyperparameter)  
- Model is TRAINED inside the fitness function  

---

## 5. Temporal Encoding (Start Hour)

**Gene = start hour (0..23).** The most flexible pattern — gene meaning depends entirely on how you simulate the 24-hour timeline.  
`num_genes = N` (items to schedule).  
`gene_space = range(24)`.

### 5A. Additive power model

```python
# SmartHomeScheduler / EVChargingSchedule
# Gene = when an appliance/EV starts
# Accumulate total power draw per hour
hourly_load = [0] * 24
for i, start in enumerate(solution):
    start = int(start)
    if start < earliest[i] or start + runtime[i] > latest[i]:
        return -9999999
    for h in range(start, start + runtime[i]):
        hourly_load[h] += power[i]

# Cost over 24 hours with solar offset + time-of-day pricing
total_cost = 0.0
for h in range(24):
    net = max(0, hourly_load[h] - solar[h])
    if net > grid_limit:
        return -9999999
    total_cost += net / 1000 * price[h]   # SmartHome: watts
    # or:  total_cost += net * price[h]   # EVCharging: kW

return -total_cost    # minimize
```

### 5B. Pairwise resource conflict model

```python
# CookingSchedule — 1 cook, 1 oven, no overlaps allowed
# Each dish: prep (cook busy) → cook (oven busy, cook free)

total_quality = 0.0
timings = []

for i, start in enumerate(solution):
    start = int(start)
    finish = start + prep[i] + cook[i]
    if finish > deadline[i]:
        return -999999

    ideal = deadline[i] - offset[i]
    dev = abs(finish - ideal)
    total_quality += quality[i] * max(0, 1 - 0.2 * dev)

    timings.append((start, start + prep[i],           # prep window
                    start + prep[i], start + prep[i] + cook[i]))  # cook window

# Pairwise overlap check — O(N²)
for i in range(N):
    for j in range(i + 1, N):
        p1, p2 = timings[i][0:2], timings[j][0:2]
        ov = max(0, min(p1[1], p2[1]) - max(p1[0], p2[0]))
        total_quality -= ov * 1000

        c1, c2 = timings[i][2:4], timings[j][2:4]
        ov = max(0, min(c1[1], c2[1]) - max(c1[0], c2[0]))
        total_quality -= ov * 1000

# Tie-breaker: earlier finish preferred
total_quality -= 0.0001 * sum(t[3] for t in timings)
return total_quality
```

### Key points
- **Additive** (SmartHome/EVCharging): `hourly[h] += power` — linear, O(24)  
- **Pairwise** (Cooking): `timings[i] vs timings[j]` — quadratic, O(N²)  
- Both share `gene_space = range(24)`, only the fitness differs  

---

## 6. Data Access: dict vs list

### When to use dict
```python
# Per-item data has NAMED fields (more than 2-3 attributes)
# Hardcoded reference data accessed by key
rooms = {1: {'name': '...', 'adjacent': [2, 7], 'value': 110}}
servers = {0: {'cpu': 8, 'ram': 16, 'bw': 10, 'cost': 5}}

# Access by key
info = rooms[room_id]
info['value']
info['adjacent']
```

### When to use flat lists
```python
# Each item has 1-2 attributes, or input is uniform fields
difficulties = [int(input()) for _ in range(N)]   # single value
times = [int(input()) for _ in range(N)]

# Multiple parallel lists (no dict)
kwh = []; arrival_hour = []; departure_hour = []
prep = []; cook = []; deadline = []; offset = []; quality = []

# Access by index
difficulties[site_id]
prep[food_idx]
```

### Dict → List conversion pattern
```python
# DICT pattern (ServerLoadBalancer)
apps.append({'cpu': cpu, 'ram': ram, 'bw': bw, 'profit': profit})
app = apps[app_idx]
app['cpu']

# LIST pattern (EVChargingSchedule) — same data, no dicts
kwh.append(k)
arrival_hour.append(a)
# Access by index
kwh[i]
```

---

## 7. Sign Convention

| Sign | Meaning | Problems | Output |
|------|---------|----------|--------|
| `return +value` | maximize fitness directly | MuseumCameras, ServerLoadBalancer, FactoryProductionPlan, MaxCrops, CityPark, CookingSchedule | `print(f'{best_fitness:.2f}')` |
| `return -value` | GA maximizes, so negate for minimization | ConstructSites, ProductionLine, FactoryMaintenance, SmartHomeScheduler, EVChargingSchedule | `print(f'{-best_fitness:.2f}')` or `print(int(-fitness))` |

```python
# Maximization: output = fitness
print(f'{best_fitness:.2f}')

# Minimization: output = -fitness
print(f'{-best_fitness:.2f}')
print(int(-best_solution_fitness))
```

---

## 8. Extraction Methods

```python
# RECOMMENDED — find best across ALL generations
best_solution, _, _ = ga.best_solution(ga.last_generation_fitness)

# ALTERNATIVE — best of last generation only
best_solution, _, _ = ga.best_solution()

# Always recompute fitness on the extracted solution
best_fitness = fitness_func(ga, best_solution, 0)
```

---

## 9. Building Custom Print Output

```python
# Per-item assignment (ConstructSites)
for site_id, team_id in enumerate(best_solution):
    print(f"Site {site_id} -> Team {int(team_id)}")

# Per-machine task list (ProductionLine)
for machine in range(K):
    tasks = [str(t) for t, m in enumerate(best_solution) if int(m) == machine]
    print(f"Machine {machine}: {' '.join(tasks)}")

# Custom coordinates (CityPark, MaxCrops)
for r, c in active_benches:
    print(f"Bench at ({r}, {c})")

for g in active_sprinklers:
    print(f"Position: {g // N}, {g % N}")
```

### Formatting reference
```python
f'{value:.2f}'               # 2 decimal places
f'{value:.1f}'               # 1 decimal place
f'{-value:.2f}'              # negated + 2 decimals
f'Optimal: {value}M$'        # custom label
int(-best_solution_fitness)  # cast to integer
```

---

## 10. Common Pitfalls

```python
# 1. numpy → int conversion (pygad passes numpy arrays)
solution = [int(x) for x in solution]

# 2. random seed for reproducibility
import random
random.seed(0)

# 3. gene_space must be a list, not range
gene_space = list(range(24))    # ✓ works in all pygad versions
gene_space = range(24)          # ✓ works in newer pygad
gene_space = [1, 2, 3, 4, 5]   # explicit list for selection

# 4. num_genes = input size
num_genes = N    # most problems — read from stdin
num_genes = K    # MuseumCameras, MaxCrops, CityPark — fixed count

# 5. Death penalty values: must be far worse than any valid solution
return -100000      # for minimization (worse than any valid -cost)
return -999999      # typical, safe for most problems
return -999999999   # extreme, use when valid values can be large

# 6. FactoryProductionPlan needs integer genes explicitly
params = {
    'gene_type': int,     # force integer genes
    'gene_space': range(16),
}

# 7. FactoryMaintenance uses np.where() — works only with numpy arrays
# Convert solution to int first
best_solution = np.round(best_solution).astype(int)
team_indices = np.where(best_solution == team_id)[0]
```

---

## 11. Parameter Template

```python
params = {
    'num_generations': 200,      # adjust based on complexity
    'sol_per_pop': 50,
    'num_parents_mating': 20,
    'num_genes': N,              # chromosome length
    'gene_space': ...,           # what values can each gene take
    'fitness_func': fitness_func,
    'mutation_num_genes': 1,     # one mutation per offspring
}
ga = pygad.GA(**params)
ga.run()
```

| Problem | generations | sol_per_pop | parents_mating |
|---------|-------------|-------------|----------------|
| MuseumCameras | 1000 | 100 | 40 |
| ProductionLine | 200 | 50 | 20 |
| FactoryProductionPlan | 300 | 50 | 20 |
| CookingSchedule | 200 | 50 | 20 |
| ParamOptimisation | 40 | 50 | 25 |
