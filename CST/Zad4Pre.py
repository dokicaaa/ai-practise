from constraint import *

if __name__ == '__main__':
    n = int(input().strip())

    problem = Problem(BacktrackingSolver())
    # Site moznie pozicii se niza od (r,c) - Domainot e ova na kralicte
    cells = [(r, c) for r in range(n) for c in range(n)]

    # Variabla e queen koj mozhe da ima range on 1 do n i domain e site cells
    # No bidejki vakov pripta dodeulva sekoj cel na sekoja kralica, se dobiva time lmiiet
    # {1: (6, 6), 2: (5, 4), 3: (4, 2), 4: (3, 0), 5: (2, 5), 6: (1, 3), 7: (0, 1)}
    # Voocuvame pattern deka sekogas q1 e vo r 6, q2 r5.....
    for queen in range(1, n + 1):
        row = n - queen  # Queen 1 gets row n-1, Queen n gets row 0

        # Only give this queen the 'n' cells that belong to her specific row
        domain = [(row, c) for c in range(n)]
        problem.addVariable(queen, domain)
    problem.addConstraint(AllDifferentConstraint(), list(range(1, n + 1)))

    # Za sekoj par kralici vidi dali se sechat, odnosno dali se ist column i row
    for q1 in range(1, n + 1):
        for q2 in range(q1 + 1, n + 1):
            problem.addConstraint(lambda a, b:
                a[0] != b[0] and  # da ne se isti row
                a[1] != b[1] and # da ne se isti col
                #Ako abs vrednost od ralziak na distance r1-r2 == c1-c2 toga tie se na doagpma;
                abs(a[0] - b[0]) != abs(a[1] - b[1]), [q1, q2])

    solutions = problem.getSolutions()

    # Ako e < 6 togash variabli ni se site mozni pozicii na samata tabla
    if n <= 6:
        print(len(solutions))
    else:
        print(problem.getSolution())



