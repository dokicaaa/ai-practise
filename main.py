from searching_framework import Problem, astar_search

class MazeProblem(Problem):
    def __init__(self, initial, goal, walls, grid_size):
        super().__init__(initial, goal)
        self.walls = set(walls)
        self.grid_size = grid_size

    def is_valid(self, c, r):
        return 0 <= c < self.grid_size and 0 <= r < self.grid_size and (c, r) not in self.walls

    def successor(self, state):
        c, r = state
        successors = {}

        if self.is_valid(c, r + 1):
            successors["Gore"] = (c, r + 1)

        if self.is_valid(c, r - 1):
            successors["Dolu"] = (c, r - 1)

        if self.is_valid(c - 1, r):
            successors["Levo"] = (c - 1, r)

        if self.is_valid(c + 1, r) and self.is_valid(c + 2, r):
            successors["Desno 2"] = (c + 2, r)

        if self.is_valid(c + 1, r) and self.is_valid(c + 2, r) and self.is_valid(c + 3, r):
            successors["Desno 3"] = (c + 3, r)

        return successors

    def h(self, node):
        c, r = node.state
        gc, gr = self.goal
        return abs(c - gc) + abs(r - gr)

    def actions(self, state):
        return list(self.successor(state).keys())

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return state == self.goal

#
# if __name__ == "__main__":
#     grid_size = int(input())
#     walls_counter = int(input())
#
#     walls = []
#     for _ in range(walls_counter):
#         parts = input().strip().split(",")
#         walls.append((int(parts[0]), int(parts[1])))
#
#     initial_parts = input().strip().split(",")
#     initial_state = (int(initial_parts[0]), int(initial_parts[1]))
#
#     goal_parts = input().strip().split(",")
#     goal = (int(goal_parts[0]), int(goal_parts[1]))
#
#     problem = MazeProblem(initial_state, goal, walls, grid_size)
#     result = astar_search(problem, problem.h)
#
#     if result is None:
#         print("No Solution!")
#     else:
#         print(result.solution())