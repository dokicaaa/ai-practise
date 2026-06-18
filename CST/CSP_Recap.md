# Constraint Satisfaction Problems — Pattern Repository

## Quick Reference

| Problem | Variables | Domain | Key Constraints |
|---------|-----------|--------|----------------|
| Cryptarithmetic (SEND+MORE=MONEY) | 8 letters (S,E,N,D,M,O,R,Y) | 0-9 | AllDifferent, S≠0, M≠0, arithmetic equation |
| Variable Sums (Zad2) | A,B,C,D,E,F | 0-100 | AllDifferent, odd(B/D/E), MinSum(A+B+C≥100), ExactSum(D+E=150), F%10%4==0 |
| Sudoku | 81 cells | 1-9 | 3×AllDifferent (rows, cols, 3×3 blocks) |
| N-Queens (n≤6) | N queens | all cells | AllDifferent, no share row/col/diag (pairwise) |
| N-Queens (n>6) | N queens | 1 row each | domain reduced to 1 row per queen |
| Meeting Scheduling (Zad5) | 4 vars | 0/1 + 12-19 | Simona=1, Simona+1 other, per-person availability |
| Tent Placement (Kol1) | M tents (one per tree) | all non-tree cells | AllDifferent, tent adjacent to its tree |
| Film Scheduling (Kol2) | 3 vars per film (day,time,cinema) | day[1..L], time[12..23], cinema[1,2] | horror≥21:00, short films same day, no overlap |
| Paper Scheduling (Zad6) | N papers | T1..Tnum | max 4 per slot, same-topic papers same slot (≤4) |
| University Timetable (Zad7) | lecture+exercise slots | day_hour strings | no_overlap(day,hour), ML different hours |
| Band Scheduling (Zad8) | N bands | S1,S2,S3 | AllDifferent for 120min bands, max 5 sub-80min per stage, same-genre same stage (≤300min) |

---

## 0. Setup

```python
from constraint import *

problem = Problem(BacktrackingSolver())

# Optional: solver selection from input
if solver_name == "BacktrackingSolver":
    solver = BacktrackingSolver()
elif solver_name == "RecursiveBacktrackingSolver":
    solver = RecursiveBacktrackingSolver()
else:
    solver = MinConflictsSolver()
problem = Problem(solver)
```

---

## 1. Variable Definition Patterns

### 1A. Simple Integer Domain
```python
problem.addVariable("X", Domain(set(range(10))))    # 0-9
problem.addVariable("X", range(101))                 # 0-100
problem.addVariable("X", [0, 1])                     # binary
```

### 1B. Multiple Variables with Same Domain
```python
variables = ["S", "E", "N", "D", "M", "O", "R", "Y"]
for var in variables:
    problem.addVariable(var, Domain(set(range(10))))

# or shorter:
problem.addVariables(variables, domain)
```

### 1C. Pre-computed Domain (Domain Reduction)
```python
# N-Queens: give each queen only its own row → drastically reduces search
all_cells = [(r, c) for r in range(n) for c in range(n)]

for queen in range(1, n + 1):
    row = n - queen                       # each queen gets a unique row
    domain = [(row, c) for c in range(n)]
    problem.addVariable(queen, domain)
```

### 1D. String-based Time Slots
```python
domain = ["Mon_11", "Mon_12", "Wed_11", "Wed_12", "Fri_11", "Fri_12"]
problem.addVariables(lecture_vars, domain)
```

### 1E. Dynamic Variable Naming
```python
# Film scheduling
for film in film_ids:
    problem.addVariable(f"{film}_day", list(range(1, l_days + 1)))
    problem.addVariable(f"{film}_time", list(range(12, 24)))

# University timetable
ai_lectures = [f"AI_lecture_{i+1}" for i in range(lecture_slots_AI)]
problem.addVariables(ai_lectures, AI_lectures_domain)
```

---

## 2. Built-in Constraints

| Constraint | Usage | What It Does |
|------------|-------|-------------|
| `AllDifferentConstraint()` | `problem.addConstraint(AllDifferentConstraint(), vars)` | All variables get different values |
| `AllEqualConstraint()` | `problem.addConstraint(AllEqualConstraint(), vars)` | All variables get the same value |
| `InSetConstraint([1])` | `problem.addConstraint(InSetConstraint([1]), ["X"])` | X must be in set {1} |
| `SomeInSetConstraint([1])` | `problem.addConstraint(SomeInSetConstraint([1]), ["A","B"])` | At least one variable in set {1} |
| `ExactSumConstraint(150)` | `problem.addConstraint(ExactSumConstraint(150), ["D","E"])` | D + E == 150 |
| `MinSumConstraint(100)` | `problem.addConstraint(MinSumConstraint(100), ["A","B","C"])` | A + B + C >= 100 |
| `MaxSumConstraint(100)` | `problem.addConstraint(MaxSumConstraint(100), ["A","B","C"])` | A + B + C <= 100 |

---

## 3. Custom Lambda Constraints

### 3A. Simple Unary Constraint
```python
problem.addConstraint(lambda S: S != 0, ["S"])            # S cannot be 0
problem.addConstraint(lambda x: x % 2 != 0, ["B"])        # B must be odd
problem.addConstraint(lambda F: (F % 10) % 4 == 0, ["F"]) # last digit divisible by 4
```

### 3B. Binary Pairwise Constraint (N-Queens)
```python
def no_attack(a, b):
    return (a[0] != b[0] and              # different row
            a[1] != b[1] and              # different column
            abs(a[0] - b[0]) != abs(a[1] - b[1]))  # different diagonal

for q1 in range(1, n + 1):
    for q2 in range(q1 + 1, n + 1):
        problem.addConstraint(no_attack, [q1, q2])
```

### 3C. Multi-Variable with `*slots` Tuple
```python
# Max 4 papers per time slot
def max_4(*slots):
    for slot in domain:        # domain = [f'T{i+1}' for i in range(num)]
        if slots.count(slot) > 4:
            return False
    return True

problem.addConstraint(max_4, variables)  # all variables passed as *slots
```

### 3D. Cryptarithmetic Equation
```python
def cryptic_check(S, E, N, D, M, O, R, Y):
    send  = 1000 * S + 100 * E + 10 * N + D
    more  = 1000 * M + 100 * O + 10 * R + E
    money = 10000 * M + 1000 * O + 100 * N + 10 * E + Y
    return send + more == money

problem.addConstraint(cryptic_check, variables)
```

### 3E. No-Overlap Scheduling (String Times)
```python
def no_overlap(time1, time2):
    day1, hour1 = time1.split('_')
    day2, hour2 = time2.split('_')
    if day1 == day2:
        if abs(int(hour1) - int(hour2)) < 2:    # <2 means overlapping hour
            return False
    return True

for i in range(len(all_variables)):
    for j in range(i + 1, len(all_variables)):
        problem.addConstraint(no_overlap, [all_variables[i], all_variables[j]])
```

### 3F. Film/Event Overlap (Numeric Times)
```python
def no_overlap(day1, time1, cinema1, day2, time2, cinema2, dur1, dur2):
    if day1 != day2 or cinema1 != cinema2:
        return True
    end1 = time1 + dur1
    end2 = time2 + dur2
    return end1 <= time2 or end2 <= time1

# Requires closure for duration values
for i in range(len(film_ids)):
    for j in range(i + 1, len(film_ids)):
        f1, f2 = film_ids[i], film_ids[j]
        dur1, dur2 = movies[f1][0], movies[f2][0]
        problem.addConstraint(
            lambda d1, t1, c1, d2, t2, c2, du1=dur1, du2=dur2:
                no_overlap(d1, t1, c1, d2, t2, c2, du1, du2),
            [f"{f1}_day", f"{f1}_time", f"{f1}_cinema",
             f"{f2}_day", f"{f2}_time", f"{f2}_cinema"]
        )
```

### 3G. Max Count Constraint (Bands per Stage)
```python
def max_5_80(*args):
    for stage in domain:                     # domain = ['S1', 'S2', 'S3']
        if args.count(stage) > 5:
            return False
    return True

bands_under_80 = [b for b, data in bands.items() if int(data[1]) < 80]
problem.addConstraint(max_5_80, bands_under_80)
```

---

## 4. Pattern: Pre-Filtering Before Adding Constraints

Always group/filter similar items before adding constraints:

```python
# Group by topic, then add AllEqual only if ≤4 papers
topic_to_papers = {}
for paper, topic in papers.items():
    if topic not in topic_to_papers:
        topic_to_papers[topic] = []
    topic_to_papers[topic].append(paper)

for topic, topic_papers in topic_to_papers.items():
    if len(topic_papers) <= 4:
        problem.addConstraint(AllEqualConstraint(), topic_papers)
```

```python
# Horror films start at ≥21:00
for film, (duration, genre) in movies.items():
    if genre == "horror":
        problem.addConstraint(lambda t: t >= 21, [f"{film}_time"])
```

```python
# Same-genre bands same stage if total time ≤ 300
for genre in ["punk", "metal", "rock"]:
    bands_in_genre = [band for band, data in bands.items() if data[0] == genre]
    total_time = sum(int(data[1]) for b, data in bands.items() if data[0] == genre)
    if total_time <= 300:
        problem.addConstraint(AllEqualConstraint(), bands_in_genre)
```

---

## 5. Pattern: 1D ↔ 2D Index Translation

```python
# Sudoku: cell index from (row, col)
cell = row * 9 + col

# Extract row cells
row_cells = [r * 9 + c for c in range(9)]

# Extract column cells
col_cells = [r * 9 + c for r in range(9)]

# Extract 3×3 block cells
for block_row in range(3):
    for block_col in range(3):
        block_cells = []
        for r in range(3):
            for c in range(3):
                cell = (block_row * 3 + r) * 9 + (block_col * 3 + c)
                block_cells.append(cell)
        problem.addConstraint(AllDifferentConstraint(), block_cells)
```

---

## 6. Meeting/Availability Pattern

```python
# Each person has availability times, attendance is binary
problem.addVariable("Simona_attendance", [0, 1])
problem.addVariable("time_meeting", range(12, 20))

# Simona must attend AND time must be in her available slots
problem.addConstraint(InSetConstraint([1]), ["Simona_attendance"])
problem.addConstraint(InSetConstraint(simona_times), ["time_meeting"])

# Marija attends only if time fits her schedule
problem.addConstraint(
    lambda m, t: m == 0 or t in marija_times,
    ["Marija_attendance", "time_meeting"]
)
```

**Print ordered solutions** (autograder may require specific key order):
```python
ordered_keys = ['Simona_attendance', 'Marija_attendance', 'Petar_attendance', 'time_meeting']
for solution in solutions:
    formatted = {key: solution[key] for key in ordered_keys}
    print(formatted)
```

---

## 7. Sudoku Pattern

```python
# 81 variables, each 1-9
for i in range(81):
    problem.addVariable(i, Domain(set(range(1, 10))))

# Row constraint
for r in range(9):
    row_cells = [r * 9 + c for c in range(9)]
    problem.addConstraint(AllDifferentConstraint(), row_cells)

# Column constraint
for c in range(9):
    col_cells = [r * 9 + c for r in range(9)]
    problem.addConstraint(AllDifferentConstraint(), col_cells)

# Block constraint
for block_row in range(3):
    for block_col in range(3):
        block_cells = []
        for r in range(3):
            for c in range(3):
                cell = (block_row * 3 + r) * 9 + (block_col * 3 + c)
                block_cells.append(cell)
        problem.addConstraint(AllDifferentConstraint(), block_cells)
```

---

## 8. Tent Placement (Kol1) Pattern

```python
# M = number of trees
# Each tent must be on a non-tree cell ADJACENT to its tree
BOARD_SIZE = 6
all_cells = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)]
tree_set = set(trees)

tent_domain = [cell for cell in all_cells if cell not in tree_set]
tent_vars = list(range(M))          # one tent per tree
problem.addVariables(tent_vars, tent_domain)

# All tents on different cells
problem.addConstraint(AllDifferentConstraint(), tent_vars)

# Each tent must be adjacent (N/S/E/W) to its tree
def h_v_neighbors(pos):
    r, c = pos
    return {(r-1,c), (r+1,c), (r,c-1), (r,c+1)}

# Then add constraint: tent position must be in neighbors of tree[i]
```

---

## 9. Output Patterns

```python
# Single solution
print(problem.getSolution())

# Count all solutions (n ≤ 6 for N-Queens)
solutions = problem.getSolutions()
print(len(solutions))

# Ordered output by variable name
sorted_papers = sorted(result.keys(), key=lambda x: int(x.replace('Paper', '')))
for paper in sorted_papers:
    print(f"{paper} ({papers[paper]}): {result[paper]}")

# "No Solution" check
if result is None:
    print("No Solution!")
```

---

## 10. Common Pitfalls

1. **Lambda captures by reference**: Always use default arguments (`du1=dur1`) in loops to freeze current values
   ```python
   # WRONG — all closures see the LAST value of dur1
   problem.addConstraint(lambda d1, t1, c1, d2, t2, c2: ..., vars)
   # RIGHT
   problem.addConstraint(lambda ..., du1=dur1, du2=dur2: ..., vars)
   ```

2. **Domain vs list**: When adding variables, both `Domain(set(range(10)))` and `range(10)` work, but `Domain` is explicit

3. **addVariables vs addVariable**: `addVariables(vars, domain)` gives all vars the same domain; `addVariable(name, domain)` for one

4. **all_variables list**: For pairwise constraints, collect ALL variables first, then iterate
   ```python
   all_variables = []
   all_variables.extend(ai_lectures + ["AI_exercises"])
   all_variables.extend(ml_lectures + ["ML_exercises"])
   for i in range(len(all_variables)):
       for j in range(i+1, len(all_variables)):
           problem.addConstraint(no_overlap, [all_variables[i], all_variables[j]])
   ```

5. **Output ordering**: Use `sorted(result.keys(), key=...)` for deterministic output
