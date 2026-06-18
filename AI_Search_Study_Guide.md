# Artificial Intelligence Search Problems: Comprehensive Study Guide & Pattern Repository

This document serves as your definitive study guide for state-space search problems. It contains a fully solved master template, your preferred validation style, specific code snippets for every major pattern we encountered, and a problem-by-problem log.

---

## 1. The Blueprint: Fully Solved Example

This is a complete, optimally structured solution for the **Ghost on Skates** problem. It serves as the master template for A* Search, demonstrating the proper class structure, state packing in the `main` block, and your preferred `is_valid` setup.

```python
import math
from searching_framework import Problem, astar_search

class GhostOnSkates(Problem):
    def __init__(self, initial, walls, n, goal=None):
        super().__init__(initial, goal)
        # Always store unhashable lists as tuples to prevent unhashable type errors
        self.walls = tuple(walls) 
        self.n = n

    # YOUR PREFERRED VALIDATION STYLE
    # Clean, separate checks for bounds, obstacles, and special rules.
    def is_valid(self, x, y):
        # 1. Check Grid Bounds
        if not (0 <= x < self.n and 0 <= y < self.n):
            return False
        # 2. Check Walls/Obstacles
        if (x, y) in self.walls:
            return False
        return True

    def successor(self, state):
        successors = dict()
        x, y = state

        # Dictionary of action names and their coordinate offsets
        # IMPORTANT: Right moves change the X coordinate, Up moves change the Y coordinate
        directions = {
            'Up 1': (0, 1),
            'Up 2': (0, 2),
            'Up 3': (0, 3),
            'Right 1': (1, 0),
            'Right 2': (2, 0),
            'Right 3': (3, 0),
        }

        for action, (dx, dy) in directions.items():
            nx, ny = dx + x, dy + y
            new_state = (nx, ny)

            # Validate before adding to successors
            if self.is_valid(nx, ny):
                successors[action] = new_state
                
        return successors

    def actions(self, state):
        return list(self.successor(state).keys())

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return state == self.goal

    def h(self, node):
        x, y = node.state
        goal_x, goal_y = self.goal

        # Float division encourages greedy tie-breaking for larger jumps.
        # Do not use math.ceil if the autograder expects the largest jumps first!
        steps_x = abs(goal_x - x) / 3
        steps_y = abs(goal_y - y) / 3

        return steps_x + steps_y

if __name__ == '__main__':
    # Parse inputs
    n = int(input().strip())
    num_walls = int(input().strip())
    
    walls = []
    for _ in range(num_walls):
        parts = input().strip().split(',')
        walls.append((int(parts[0]), int(parts[1])))

    # Always pack the initial state into a single tuple before passing to the class
    initial_state = (0, 0)
    goal_state = (n - 1, n - 1)

    # Initialize problem and run search
    problem = GhostOnSkates(initial_state, walls, n, goal_state)
    result = astar_search(problem)

    if result:
        print(result.solution())
    else:
        print("No solution found")
```

---

## 2. Core State Representation Patterns

### A. The "Phase Tracker" (e.g., Robot & Machines M1/M2)
**Concept:** Tracking sequential multi-step tasks where progress resets on interruption. The robot must repair M1 completely before starting M2.

```python
# State: (x, y, m1_parts_left, m2_parts_left, m1_progress, m2_progress)

def successor(self, state):
    succ = {}
    x, y, m1_parts, m2_parts, m1_rep, m2_rep = state

    for action, (dx, dy) in directions.items():
        new_x, new_y = dx + x, dy + y
        if not self.is_valid(new_x, new_y):
            continue

        new_m1_parts = list(m1_parts)
        new_m2_parts = list(m2_parts)

        # The Ternary Reset Pattern — reset to 0 if interrupted
        new_m1_rep = 0 if m1_rep < self.m1_steps else self.m1_steps
        new_m2_rep = 0 if m2_rep < self.m2_steps else self.m2_steps

        # Phase 1: collect M1 parts
        if m1_rep < self.m1_steps:
            if (new_x, new_y) in new_m1_parts:
                new_m1_parts.remove((new_x, new_y))
        else:
            # Phase 2: collect M2 parts (after M1 is done)
            if (new_x, new_y) in new_m2_parts:
                new_m2_parts.remove((new_x, new_y))

        # Re-pack and sort to prevent state duplication
        succ[action] = (new_x, new_y,
                        tuple(sorted(new_m1_parts)),
                        tuple(sorted(new_m2_parts)),
                        new_m1_rep, new_m2_rep)

    # Repair action — only when standing on the machine with no parts left
    if m1_rep < self.m1_steps:
        if (x, y) == self.m1_pos and len(m1_parts) == 0:
            succ['Repair'] = (x, y, m1_parts, m2_parts, m1_rep + 1, m2_rep)
    elif m2_rep < self.m2_steps:
        if (x, y) == self.m2_pos and len(m2_parts) == 0:
            succ['Repair'] = (x, y, m1_parts, m2_parts, m1_rep, m2_rep + 1)
    return succ

def goal_test(self, state):
    # Both machines fully repaired
    return state[4] == self.m1_steps and state[5] == self.m2_steps
```

### B. The "Flat Grid" (e.g., Lights Out)
**Concept:** A 2D board flattened into a 1D tuple. Flipping states across an entire board.
```python
# State Representation: (1, 0, 0, 1, 1, 0, ...) length N^2

# Inside successor():
for r in range(self.n):
    for c in range(self.n):
        action = f'x: {r}, y: {c}'
        new_state = list(state)
        
        # Calculate valid flips (handling bounds carefully)
        flips = [(r, c)]
        if r > 0: flips.append((r - 1, c))           # Up
        if r < self.n - 1: flips.append((r + 1, c))  # Down
        if c > 0: flips.append((r, c - 1))           # Left
        if c < self.n - 1: flips.append((r, c + 1))  # Right
        
        # The 2D to 1D Math Trick
        for flip_r, flip_c in flips:
            idx = flip_r * self.n + flip_c
            new_state[idx] = 1 - new_state[idx] # Toggle 0/1 (or flip value)
            
        succ[action] = tuple(new_state)
```

### C. The "Permutation Tuple" (e.g., Disks on a Strip)
**Concept:** Multiple entities moving on a 1D line to a sorted goal. Order of actions matters.
```python
# State Representation: (1, 2, 3, 0, 0, 0, 0)

# Inside successor():
for i in range(self.L): # Sequential iteration guarantees strict output order for autograders
    if state[i] != 0:
        disk = state[i]
        
        # R2 Pattern: Jump OVER a disk (!= 0) into an empty space (== 0)
        if i + 2 < self.L and state[i + 1] != 0 and state[i + 2] == 0:
            new_state = list(state)
            
            # Parallel swap for easy movement
            new_state[i], new_state[i + 2] = new_state[i + 2], new_state[i]
            succ[f'R2: Disk {disk}'] = tuple(new_state)
```

### D. The "Multi-Segment Entity" (e.g., Snake)
**Concept:** Moving an entity that takes up multiple tiles and grows when it consumes items.
```python
# State Representation: (body_tuple, direction, apples_tuple)

# Inside successor():
new_head = (head_x + dx, head_y + dy)
new_g_apples = list(g_apples)

if new_head in new_g_apples:
    new_g_apples.remove(new_head)
    # Grow: Add new head to the front, keep the entire old body
    new_body = (new_head,) + body
else:
    # Move normally: Add new head, slice off the last element (tail)
    new_body = (new_head,) + body[:-1]

new_state = (new_body, new_dir, tuple(new_g_apples))
```

### E. The "Timer + Hazard" Pattern (e.g., Laser)
**Concept:** A hazard (laser) is active every N ticks. A timer cycles 1→4→1, and when timer=4 the laser kills the player if they share a row or column with it. The laser also FOLLOWS the player (moves to player's position when timer=1).

```python
# State: (player_x, player_y, laser_x, laser_y, timer)

def successor(self, state):
    succ = {}
    (x, y), (lx, ly), timer = state

    dirs = {"Gore": (0, 1), "Dolu": (0, -1),
            "Levo": (-1, 0), "Desno": (1, 0), "Stoj": (0, 0)}

    for action, (dx, dy) in dirs.items():
        nx, ny = dx + x, dy + y

        # Timer cycles: 1→2→3→4→1
        nt = timer + 1 if timer < 4 else 1

        # Laser moves to player's position when timer resets to 1
        if nt == 1:
            nlx, nly = nx, ny     # laser teleports to new player pos
        else:
            nlx, nly = lx, ly     # laser stays put

        if self.is_valid(nx, ny, nt, nlx, nly):
            succ[action] = ((nx, ny), (nlx, nly), nt)
    return succ

def is_valid(self, px, py, nt, lx, ly):
    # Bounds + obstacle check
    if not (0 <= px < M and 0 <= py < N):
        return False
    if (px, py) in self.blocked:
        return False
    # Laser kills if timer=4 and player has same row or col as laser
    if nt == 4 and (px == lx or py == ly):
        return False
    return True
```

### F. The "Moving Target" Pattern (e.g., Climbing / Moving House)
**Concept:** The target (house) moves independently each step. The player must catch it. State tracks both positions and the house's direction.

```python
# State: ((px, py), (hx, hy), direction)
# House moves: bounces left↔right. Direction flips at walls (x=0 or x=W-1).

def move_house(self, hx, direction):
    if direction == "right":
        if hx + 1 >= self.W:
            return hx - 1, "left"
        return hx + 1, "right"
    else:
        if hx - 1 < 0:
            return hx + 1, "right"
        return hx - 1, "left"

def successor(self, state):
    succ = {}
    (px, py), (hx, hy), direction = state

    nhx, n_dir = self.move_house(hx, direction)  # house always moves 1
    new_house = (nhx, hy)

    person_moves = {
        "Wait": (0, 0),
        "Up 1": (0, 1), "Up 2": (0, 2),
        "Up-right 1": (1, 1), "Up-right 2": (2, 2),
        "Up-left 1": (-1, 1), "Up-left 2": (-2, 2),
    }

    for action, (dx, dy) in person_moves.items():
        npx, npy = (px + dx), (py + dy)
        if self.is_valid(npx, npy, nhx, hy):  # catch check in is_valid
            succ[action] = ((npx, npy), new_house, n_dir)
    return succ

def goal_test(self, state):
    (px, py), (hx, hy), direction = state
    return (px, py) == (hx, hy)                # caught the house

def is_valid(self, px, py, hx, hy):
    # If on top row, only valid if player is exactly on house
    if py == self.H - 1:
        return (px, py) == (hx, hy)
    return (px, py) in allowed and 0 <= px < self.W
```

---

## 3. Heuristic Design Patterns (A* Search)

### A. The "Variable Speed" Pattern (e.g., Ghost / Sprints)
**Concept:** The agent can move more than 1 tile per step (e.g., sprint 3 tiles). Using standard Manhattan distance will overestimate the cost.
```python
def h(self, node):
    x, y = node.state
    goal_x, goal_y = self.goal
    
    # Float division breaks ties optimally by prioritizing larger jumps.
    # Do not use math.ceil() if the autograder requires greedy largest-jump paths.
    steps_x = abs(goal_x - x) / 3.0
    steps_y = abs(goal_y - y) / 3.0
    return steps_x + steps_y
```

### B. The "Independent Entity Sum" Pattern (e.g., 5 Squares to Diagonal)
**Concept:** Multiple independent entities moving to specific calculated positions.
```python
def h(self, node):
    state = node.state
    total_distance = 0
    
    for i, (x, y) in enumerate(state):
        # Diagonal goal math trick based on index (e.g., top-left to bottom-right)
        goal_x = i
        goal_y = 4 - i
        
        # Because they don't block each other, we can safely SUM the Manhattan distances
        total_distance += abs(x - goal_x) + abs(y - goal_y)
        
    return total_distance
```

### C. The "Multiple Targets" Pattern (e.g., Snake & Apples)
**Concept:** Collecting multiple items on a map in the minimum number of steps.
```python
def h(self, node):
    body, direction, g_apples = node.state
    if not g_apples: 
        return 0
        
    hx, hy = body[0]
    
    # CRITICAL: To remain optimistic (admissible), NEVER sum the distances to all apples.
    # You might eat one apple on the way to another. 
    # Always take the MAXIMUM distance to a single remaining apple.
    distances = [abs(apple_x - hx) + abs(apple_y - hy) for apple_x, apple_y in g_apples]
    return max(distances)
```

### D. The "Remaining Rows" Pattern (e.g., Climbing / Moving House)
**Concept:** The player can only move upward. The number of rows remaining divided by max jump height gives an admissible heuristic.

```python
def h(self, node):
    (px, py), (hx, hy), direction = node.state
    rows_remaining = (self.H - 1) - py
    return rows_remaining // 2       # max upward jump is 2
```

### E. The "Custom Step Division" Pattern (e.g., Zad1 Variable Speed)
**Concept:** The agent can move 1, 2, or 3 tiles right, but only 1 tile in other directions. Calculate exact minimum steps using division with remainder analysis.

```python
def h(self, node):
    x, y = node.state
    goal_x, goal_y = self.goal

    # Horizontal: jumps of 3 with remainder handling
    dx = abs(x - goal_x)
    horizontal_cost = dx // 3
    remaining = dx % 3
    if remaining == 2:
        horizontal_cost += 1
    elif remaining == 1:
        horizontal_cost += 1

    # Vertical: only 1 tile per step
    dy = abs(y - goal_y)

    return horizontal_cost + dy
```
