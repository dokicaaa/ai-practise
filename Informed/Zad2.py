from searching_framework import Problem, astar_search

# fixxed 5x9

# samo kade sto ima polinhja, tamu ze dvizi
# mozhe da ostane naisto pole

# kukjata se dvizhi, levo i desno vo sekoj state -> odi vo state |
# koga ke stigne do 0 menuva nasoka i koga ke sitnge do 5 levo
# pocetna nasoka na kukickata se chita od vlez

# statte (px, py, hx, hy, direction house)

class ClimbingProblem(Problem):
    def __init__(self, initial, goal, allowed, width=5, height=9):
        super().__init__(initial, goal)
        self.allowed = allowed
        self.W = width
        self.H = height

    def is_valid(self, px, py, hx, hy):
        if py == self.H - 1:
            return (px, py) == (hx, hy)
        return (px, py) in allowed and 0 <= px < self.W

    def goal_test(self, state):
        (px, py), (hx, hy), direction = state
        return (px, py) == (hx, hy)

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

        nhx, n_dir = self.move_house(hx, direction)
        new_house = (nhx, hy)

        person_moves = {
            "Wait": (0, 0),
            "Up 1": (0, 1),
            "Up 2": (0, 2),
            "Up-right 1": (1, 1),
            "Up-right 2": (2, 2),
            "Up-left 1": (-1, 1),
            "Up-left 2": (-2, 2),
        }

        for action, (dx, dy) in person_moves.items():
            npx, npy = (px + dx), (py + dy)
            if self.is_valid(npx, npy, nhx, hy):
                new_state = ((npx, npy), new_house, n_dir)
                succ[action] = new_state
        return succ

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def h(self, node):
        (px, py), (hx, hy), direction = node.state
        rows_remaining = (self.H - 1) - py
        return rows_remaining // 2

if __name__ == '__main__':
    allowed = [(1, 0), (2, 0), (3, 0), (1, 1), (2, 1), (0, 2), (2, 2), (4, 2), (1, 3), (3, 3), (4, 3), (0, 4), (2, 4),
               (2, 5), (3, 5), (0, 6), (2, 6), (1, 7), (3, 7)]

    person_parts = input().split(',')
    person = (int(person_parts[0]), int(person_parts[1]))

    house_parts = input().split(',')
    house = (int(house_parts[0]), int(house_parts[1]))

    direction = input().strip()

    initial = (person, house, direction)

    problem = ClimbingProblem(initial, None, allowed)
    result = astar_search(problem, h=lambda node: problem.h(node))

    if result:
        print(result.solution())
    else:
        print("No solution found")
