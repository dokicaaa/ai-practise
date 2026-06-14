from searching_framework import *


# from utils import *
# from uninformed_search import *
# from informed_search import *


# mozhe da stavi ako e vo bilo koe sosdenoo
# ne smee da stapne na poel vo koja ima kutija,
# vo sekoja kutija ima tocno 1 topka
# state = px,py, walls


class Boxes(Problem):
    def __init__(self, initial, goal=None, n=0, boxes=None):
        super().__init__(initial, goal)
        self.boxes = boxes or set()
        self.n = n

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def goal_test(self, state):
        (px, py), remaining = state
        return len(remaining) == 0

    def is_valid(self, x, y):
        return 0 <= x < self.n and 0 <= y < self.n and (x, y) not in self.boxes

    def successor(self, state):
        succ = {}
        (x, y), remaining_boxes = state
        directions = {
            "Gore": (0, 1),
            "Desno": (1, 0)
        }

        for direction, (dx, dy) in directions.items():
            nx = x + dx
            ny = y + dy

            if self.is_valid(nx, ny):
                new_boxes = []
                for bx, by in remaining_boxes:
                    if max(abs(bx - nx), abs(by - ny)) > 1:
                        new_boxes.append((bx, by))

                new_state = ((nx, ny), tuple(new_boxes))
                succ[direction] = new_state
        return succ


if __name__ == '__main__':
    n = int(input())
    man_pos = (0, 0)

    num_boxes = int(input())
    boxes = list()
    for _ in range(num_boxes):
        boxes.append(tuple(map(int, input().split(','))))

    initial_state = (man_pos, tuple(boxes))

    problem = Boxes(initial_state, goal=None, n=n, boxes=boxes)

    result = breadth_first_graph_search(problem)
    if result:
        print(result.solution())
    else:
        print("No Solution!")
