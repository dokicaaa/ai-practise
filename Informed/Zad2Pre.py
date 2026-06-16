import math

from searching_framework import Problem, astar_search

# STATE 0> (px,py, hx, direction)
class ClimbingP(Problem):
        def __init__(self, initial, goal, allowed, w=5, h=9):
            super().__init__(initial, goal)
            self.allowed = allowed
            self.W = w
            self.H = h

        def is_valid(self, hx, hy, px, py):
            # Ako choveceto e na posleden red vrakjash dali e na isto pole vo ist moment
            if py == self.H - 1:
                return (px, py) == (hx, hy)
            return (px, py) in self.allowed and 0 <= px <= self.W


        #House mooves right to left. Consider starging direcition
        def move_house(self, hx, direction):
            # Ako se dvziiz desno
            if direction == "right":
                # Ako sledniot space ne e pogolem od bounds
                if hx + 1 >= self.W:
                    # Returnash kordinata levo i smena na nasoka
                    return hx - 1, "left"
                return hx + 1, "right"
            else:
                if hx - 1 < 0:
                    return hx + 1, "right"
                return hx - 1, "left"

        def goal_test(self, state):
            (px, py), (hx, hy), direction = state
            return (px, py) == (hx, hy)

        def successor(self, state):
            succ = {}
            (px, py), (hx, hy), direction = state

            #Moove the house with our fucnion and create new state
            nhx, ndir = self.move_house(hx, direction)
            new_house = (nhx, hy)

            directions = {
                'Wait': (0,0),
                'Up 1': (0, 1),
                'Up 2': (0, 2),
                'Up-right 1': (1, 1),
                'Up-right 2': (2, 2),
                'Up-left 1': (-1, 1),
                'Up-left 2': (-2, 2),
            }

            for action, (dx, dy) in directions.items():
                nx, ny = dx + px, dy + py

                # Check if valid
                if self.is_valid(nhx, hy, nx, ny):
                    succ[action] = ((nx, ny), new_house, ndir)
            return succ

        def actions(self, state):
            return self.successor(state).keys()

        def result(self, state, action):
            return self.successor(state)[action]

        def h(self, node):
            (px, py), (hx, hy), direction = node.state
            # Maximum speed e 2 znaci everistikata mroaa da e /2
            # General fomrula - remaing rows from person to house / max moovement amount
            remaining_vertical = abs(hy - py)
            return math.ceil(remaining_vertical // 2)



if __name__ == '__main__':
    allowed = [(1, 0), (2, 0), (3, 0), (1, 1), (2, 1), (0, 2), (2, 2), (4, 2), (1, 3), (3, 3), (4, 3), (0, 4), (2, 4),
               (2, 5), (3, 5), (0, 6), (2, 6), (1, 7), (3, 7)]

    # your code here
    person_parts = input().split(',')
    person = (int(person_parts[0]), int(person_parts[1]))

    house_parts = input().split(',')
    house = (int(house_parts[0]), int(house_parts[1]))

    direction = input().strip()

    initial_state = (person, house, direction)
    problem = ClimbingP(initial_state, None, allowed)
    result = astar_search(problem, h=lambda node: problem.h(node))

    if result:
        print(result.solution())
    else:
        print("No solution found")

