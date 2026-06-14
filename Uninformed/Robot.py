from searching_framework import *

# NxN - 10 na 10

# State -> (x y, m1_parts_left, m2_parts_left2, m1_repaired, m2_repaired) - int vrednost 0 1
# dali e popravena
class Robot(Problem):
    def __init__(self, initial, walls, m1_pos, m1_steps, m2_pos, m2_steps):
        super().__init__(initial)
        self.walls = tuple(walls)
        self.m1_pos = m1_pos
        self.m1_steps = m1_steps
        self.m2_pos = m2_pos
        self.m2_steps = m2_steps

    def actions(self, state):
        return self.successor(state).keys()

    def is_valid(self, x, y):
        if not (0 <= x < 10 and 0 <= y < 10) or (x, y) in self.walls:
            return False
        return True

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        m1_rep = state[4]
        m2_rep = state[5]
        # Machines are repred when both reach neede parts_M1
        return m1_rep == self.m1_steps and m2_rep == self.m2_steps

    def successor(self, state):
        succ = {}
        x, y, m1_parts, m2_parts, m1_rep, m2_rep = state

        directions = {"Up": (0, +1), "Down": (0, -1), "Left": (-1, 0), "Right": (+1, 0)}

        for action, (dx, dy) in directions.items():
            new_x, new_y = dx + x, dy + y

            # Ako ne validno samo continiue
            if not self.is_valid(new_x, new_y):
                continue

            new_m1_parts = list(m1_parts)
            new_m2_parts = list(m2_parts)

            # If we robot is interupted repairs reset to 0:
            new_m1_rep = 0 if m1_rep < self.m1_steps else self.m1_steps
            new_m2_rep = 0 if m2_rep < self.m2_steps else self.m2_steps

            # Check if m1 is repared before m2
            if m1_rep < self.m1_steps:
            #Here we have to finish m1
                if(new_x, new_y) in new_m1_parts:
                    new_m1_parts.remove((new_x, new_y))
            else:
                # M2 can start
                if (new_x, new_y) in new_m2_parts:
                    new_m2_parts.remove((new_x, new_y))

            # build the new state
            succ[action] = (
                new_x,
                new_y,
                tuple(sorted(new_m1_parts)),
                tuple(sorted(new_m1_parts)),
                new_m1_rep,
                new_m2_rep
            )

        # We have to check if its a repapir actions
        if m1_rep < self.m1_steps:
            # If robot is on the machine 1 cordinate
            if(x,y) == self.m1_pos and len(m1_parts) == 0:
                succ['Repair'] = (x, y, m1_parts, m2_parts, m1_rep + 1, m2_rep)
        elif m2_rep < self.m2_steps:
            # If robot is on the machine 2 cordinate
            if (x, y) == self.m2_pos and len(m2_parts) == 0:
                succ['Repair'] = (x, y, m1_parts, m2_parts, m1_rep, m2_rep + 1)
        return succ



if __name__ == '__main__':
    robot_start_pos = tuple(map(int, input().split(',')))
    M1_pos = tuple(map(int, input().split(',')))
    M1_steps = int(input())
    M2_pos = tuple(map(int, input().split(',')))
    M2_steps = int(input())
    parts_M1 = int(input())
    to_collect_M1 = tuple([tuple(map(int, input().split(','))) for _ in range(parts_M1)])
    parts_M2 = int(input())
    to_collect_M2 = tuple([tuple(map(int, input().split(','))) for _ in range(parts_M2)])

    walls = [(4, 0), (5, 0), (7, 5), (8, 5), (9, 5), (1, 6), (1, 7), (0, 6), (0, 8), (0, 9), (1, 9), (2, 9), (3, 9)]


    initial_state = (
        robot_start_pos[0],
        robot_start_pos[1],
        tuple(sorted(to_collect_M1)),
        tuple(sorted(to_collect_M2)),
        0,
        0
    )
    problem = Robot(initial_state, walls, M1_pos, M1_steps, M2_pos, M2_steps)
    result = breadth_first_graph_search(problem)

    if result:
        print(result.solution())
    else:
        print("No Solution!")
