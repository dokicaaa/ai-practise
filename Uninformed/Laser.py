from searching_framework import *



# State - > ((x,y),(timer_x, timer_y), timer)
class Laser(Problem):
    def __init__(self, initial, blocked, n, m, goal = None):
        super().__init__(initial, goal)
        self.blocked = tuple(blocked)
        self.N = n
        self.M = m

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def is_valid(self, px, py, nt, lx, ly):
        # Check grid bounds
        if not (0 <= px < self.M and 0 <= py < self.N):
            return False

        # Check walls obstiacles
        if (px, py) in self.blocked:
            return False

        # if timer is 4 person cant be in same column or row as laser
        if nt == 4:
            if px == lx or py == ly:
                return False
        return True
    def goal_test(self, state):
        x, y = state[0]
        return (x, y) == self.goal

    def successor(self, state):
        succ = {}
        (x,y), (lx, ly), timer = state

        dirs = {"Gore": (0, +1), "Dolu": (0, -1), "Levo": (-1, 0), "Desno": (+1, 0), "Stoj": (0, 0)}

        for action, (dx, dy) in dirs.items():
            nx, ny = dx + x, dy + y
            # Treba da go sredime timerot da se zgolemuva

            # Increment timer each state
            # ako timer stigne 4 reset back to 0
            nt = timer + 1 if timer < 4 else 1

            # Evaluete od nov timer
            if nt == 1:
                nlx, nly = nx, ny
            else:
                nlx, nly = lx, ly

            if self.is_valid(nx, ny, nt, nlx, nly):
                succ[action] = ((nx, ny), (nlx, nly), nt)
        return succ

read_two = lambda: tuple(map(int, input().split()))
if __name__ == '__main__':
    N, M = read_two()
    man_pos = read_two()
    target_pos = read_two()
    timer = int(input())
    laser_pos = read_two()
    blocked = [read_two() for _ in range(int(input()))]

    initial_state = (man_pos, laser_pos, timer)

    problem = Laser(initial_state, blocked, N, M, target_pos)

    result = breadth_first_graph_search(problem)

    if result:
        print(result.solution())
    else:
        print("No Solution!")
