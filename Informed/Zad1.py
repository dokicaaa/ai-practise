from searching_framework import Problem, astar_search


# NxN lavirint - read from n
# not hit walls
# in bounds
# can move 2/3 positions to the rigth, the rest +1
# obbsitcles - read from input

class MazeProblem(Problem):
    def __init__(self, initial, walls, goal, n):
        super().__init__(initial, goal)
        self.walls = walls
        self.n = n

    def is_valid(self, x, y):
        return 0 <= x < self.n and 0 <= y < self.n and (x, y) not in self.walls

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return state == self.goal

    def successor(self, state):
        succ = {}

        x, y = state

        directions = {
            "Up": (0, 1),
            "Down": (0, -1),
            "Left": (-1, 0)
        }

        for direction, (dx, dy) in directions.items():
            nx = x + dx
            ny = y + dy

            if self.is_valid(nx, ny):
                new_state = (nx, ny)
                succ[f"{direction}"] = new_state

            # Right 2
            if self.is_valid(x + 1, y) and self.is_valid(x + 2, y):
                succ["Right 2"] = (x + 2, y)

            if self.is_valid(x + 1, y) and self.is_valid(x + 2, y) and self.is_valid(x + 3, y):
                succ["Right 3"] = (x + 3, y)

        return succ

    def h(self, node):
        x, y = node.state
        goal_x, goal_y = self.goal

        dx = abs(x - goal_x)
        horizontal_cost = dx // 3
        remaining = dx % 3
        if remaining == 2:
            horizontal_cost += 1
        elif remaining == 1:
            horizontal_cost += 1

        dy = abs(y - goal_y)

        return horizontal_cost + dy


if __name__ == '__main__':

    grid_size = int(input())
    num_walls = int(input())
    walls = set()
    for _ in range(num_walls):
        parts = input().split(',')
        walls.add((int(parts[0]), int(parts[1])))

    person_parts = input().split(',')
    person = (int(person_parts[0]), int(person_parts[1]))

    house_parts = input().split(',')
    house = (int(house_parts[0]), int(house_parts[1]))

    problem = MazeProblem(person, walls, house, grid_size)
    result = astar_search(problem, h=lambda node: problem.h(node))

    if result:
        print(result.solution())
    else:
        print("No solution found")
