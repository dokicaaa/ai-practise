from searching_framework import Problem, breadth_first_graph_search

class Football(Problem):
    def __init__(self, initial):
        super().__init__(initial, None)
        self.opponents = ((3, 3), (5, 4))
        self.goals = ((7, 2), (7, 3))


    def goal_test(self, state):
        man, ball = state
        return ball in self.goals

    def check_valid(self, state):
        man, ball = state
        man_x, man_y = man
        ball_x, bal_y = ball

        for x,y in [man, ball]:
            if x < 0 or x >= 8 or y < 0 or y >= 6:
                return False

        if man == ball:
            return False

        for opp_x, opp_y in self.opponents:
            if man == (opp_x, opp_y):
                return False

            if max(abs(ball_x - opp_x), abs(bal_y - opp_y)) <= 1:
                return False

        return True

    def successor(self, state):
        succ = {}
        man, ball = state
        man_x, man_y = man

        directions = {
            "up": (0, 1),
            "down": (0, -1),
            "right": (1, 0),
            "down-right": (1, -1),
            "up-right": (1, 1),

        }

        for direction_name, (dx, dy) in directions.items():
            new_m_x = man_x + dx
            new_m_y = man_y + dy
            new_man_pos = (new_m_x, new_m_y)

            if new_man_pos == ball:
                bx, by = ball
                new_ball_pos = (bx + dx, by + dy)
                new_state = (new_man_pos, new_ball_pos)
                if self.check_valid(new_state):
                    succ[f"Push ball {direction_name}"] = new_state
            else:
                new_state = (new_man_pos, ball)
                if self.check_valid(new_state):
                    succ[f"Move man {direction_name}"] = new_state
        return succ

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]


if __name__ == '__main__':
    line1 = input().split(',')
    man_pos = (int(line1[0]), int(line1[1]))

    line2 = input().split(',')
    ball_pos = (int(line2[0]), int(line2[1]))

    initial_state = (man_pos, ball_pos)

    football_problem = Football(initial_state)

    result_node = breadth_first_graph_search(football_problem)

    if result_node is None:
        print("No Solution!")
    else:
        print(result_node.solution())



