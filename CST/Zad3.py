from constraint import *

if __name__ == '__main__':
    solver_name = input().strip()

    if solver_name == "BacktrackingSolver":
        solver = BacktrackingSolver()
    elif solver_name == "RecursiveBacktrackingSolver":
        solver = RecursiveBacktrackingSolver();
    else:
        solver = MinConflictsSolver()

    problem = Problem(solver)

    for i in range(81):
        problem.addVariable(i, range(1,10))

    # ---------------------------------------
    # 1. Each row must have diff values
    for r in range(9):
        row_cells = [r * 9 + c for c in range(9)]
        problem.addConstraint(AllDifferentConstraint(), row_cells)

    # 2. Each columng must have diff values

    for c in range(9):
        col_cells = [c * 9 + c for c in range(9)]
        problem.addConstraint(AllDifferentConstraint(), col_cells)

    # 3.No repeating in one block
    for block_row in range(3):
        for block_column in range(3):
            block_cells = []
            for r in range(3):
                for c in range(3):
                    cell = (block_row * 3 + r) * 9 + (block_column * 3 + c)
                    block_cells.append(cell)
            problem.addConstraint(AllDifferentConstraint(), block_cells)

    print(problem.getSolution())