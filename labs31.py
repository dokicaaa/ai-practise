from constraint import Problem, BacktrackingSolver


def solveProblem(K, table):
    problem = Problem(BacktrackingSolver())

    # Tupple for tracking which i,j values have stars in the grid
    variables = []
    for i in range(K):
        for j in range(K):
            var = (i,j)
            variables.append(var)
            problem.addVariable(var, [0, 1])

    # Setting the regions for the gird
    regions = set()
    for i in range(K):
        for j in range(K):
            regions.add(table[i][j])
    N = len(regions)

    region_cells = {}
    for i in range(K):
        for j in range(K):
            r = table[i][j]
            region_cells.setdefault(r, []).append((i, j))

    # CONSTRAINTS

    # Constraint, must have N stars
    problem.addConstraint(lambda  *vals: sum(vals) == N, variables)

    # Maximum 2 stars per region
    for r in region_cells:
        problem.addConstraint(lambda *vals: sum(vals) <= 2, region_cells[r])

    # No two starts in teh same row
    for i in range(K):
        for j1 in range(K):
            for j2 in range(j1+1, K): #for each other cell to the right
                if table[i][j1] != table[i][j2]: #if different regions then add constraint
                    problem.addConstraint(
                        lambda x, y: not (x == 1 and y == 1), #both cant have stars, value of 1
                        [(i, j1), (i, j2)]
                    )

    # No two starts in teh same columng
    for j in range(K):
        for i1 in range(K):
            for i2 in range(i1 + 1, K):  # for each other cell down of current cell
                if table[i1][j] != table[i2][j]:  # if different regions then add constraint
                    problem.addConstraint(
                        lambda x, y: not (x == 1 and y == 1),  # both cant have stars, value of 1
                        [(i1, j), (i2, j)]
                    )

    # No adjacency in within the same group
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for i in range(K):
        for j in range(K):
            for di, dj in directions:
                # cell up,down, left, to the right of curr cell
                ni, nj = i + di, j + dj
                # if withing bound of grid
                if 0 <= ni < K and 0 <= nj < K:
                    if table[i][j] == table[ni][nj]:
                        problem.addConstraint(
                            lambda x, y: not (x == 1 and y == 1),
                            [(i, j), (ni, nj)]
                        )
    return problem.getSolution()

if __name__ == '__main__':
    K = int(input())
    grid = [list(map(int, input().split())) for _ in range(K)]

    solution = solveProblem(K, grid)

    if solution is None:
        print("No Solution!")
    else:
        for i in range(K):
            row = []
            for j in range(K):
                if solution[(i,j)] == 1:
                    row.append("*")
                else:
                    row.append(str(grid[i][j]))
            print(" ".join(row))

