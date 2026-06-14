from searching_framework import *


class Laser(Problem):
    def __init__(self, initial, goal, allowed):
        super().__init__(initial, goal)
        self.allowed = allowed

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        return state[0] == self.goal

    def is_valid(self, x, y):
        return (x,y) in self.allowed

    def successor(self, state):
        succ = {}
        (x, y), (lx, ly), t = state
        directions = {
            "Gore": (0, 1),
            "Dolu": (0, -1),
            "Levo": (-1, 0),
            "Desno": (1, 0),
            "Stoj": (0, 0)
        }

        for direction, (dx, dy) in directions.items():
            nx = x + dx
            ny = y + dy

            if self.is_valid(nx, ny):
                if t < 5:
                    nt = t + 1
                else:
                    nt = 1
                nlx, nly = lx, ly

                is_valid_Laser = True

                if nt == 2:
                    nlx, nly = nx, ny
                elif nt == 5:
                    if nx != nlx and ny != nly:
                        is_valid_Laser = False

                if is_valid_Laser:
                    succ[direction] = ((nx, ny), (nlx, nly), nt)

        return succ

read_two = lambda: tuple(map(int, input().split()))
if __name__ == '__main__':
    N, M = read_two()
    man_pos = read_two()
    target_pos = read_two()
    timer = int(input())
    laser_pos = read_two()
    allowed = [read_two() for _ in range(int(input()))]

    initial_state = (man_pos, target_pos, timer)

    problem = Laser(initial_state, target_pos, allowed)

    result = breadth_first_graph_search(problem)

    if result:
        print(result.solution())
    else:
        print("No Solution!")
