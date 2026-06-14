from constraint import *

if __name__ == '__main__':
    n = int(input())

    all_cells = [(r, c) for r in range(n) for c in range(n)]

    if n <= 6:
        problem = Problem(BacktrackingSolver())

        for queen in range(1, n + 1):
            problem.addVariable(queen, all_cells)

        problem.addConstraint(AllDifferentConstraint(), list(range(1, n + 1)))

        for q1 in range(1, n + 1):
            for q2 in range(q1 + 1, n + 1):
                problem.addConstraint(
                    lambda a, b: (
                        a[0] != b[0] and          # different row
                        a[1] != b[1] and          # different column
                        abs(a[0] - b[0]) != abs(a[1] - b[1])  # different diagonal
                    ),
                    [q1, q2]
                )

        solutions = problem.getSolutions()
        print(len(solutions))

    else:
        # ── Return only the FIRST solution ────────────────────────────
        problem = Problem(BacktrackingSolver())

        for queen in range(1, n + 1):
            problem.addVariable(queen, all_cells)

        problem.addConstraint(AllDifferentConstraint(), list(range(1, n + 1)))

        for q1 in range(1, n + 1):
            for q2 in range(q1 + 1, n + 1):
                problem.addConstraint(
                    lambda a, b: (
                        a[0] != b[0] and
                        a[1] != b[1] and
                        abs(a[0] - b[0]) != abs(a[1] - b[1])
                    ),
                    [q1, q2]
                )

        print(problem.getSolution())