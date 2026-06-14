from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())

    # ----------------------------------------------------
    # ---Prochitajte gi informaciite od vlezot
    M = int(input())
    trees = []
    for _ in range(M):
        r, c = map(int, input().split())
        trees.append((r, c))
    # -----------------------------------------------------
    # ---Izberete promenlivi i domeni so koi bi sakale da rabotite-----
    BOARD_SIZE = 6
    all_cells = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)]
    tree_set = set(trees)

    # domain sekoe pole koe ne e drvo
    tent_domain = [cell for cell in all_cells if cell not in tree_set]

    tent_vars = list(range(M))
    problem.addVariables(tent_vars, tent_domain)

    # -----------------------------------------------------
    # ---Potoa dodadete ogranichuvanjata-------------------

    problem.addConstraint(AllDifferentConstraint, tent_vars)

    def h_v_neighbors(pos):
        r, c = pos
        return {(r-1,c), (r+1,c), (r,c-1), (r,c+1)}


    # -----------------------------------------------------
    # ---Potoa pobarajte reshenie--------------------------

    solution = problem.getSolution()

    # -----------------------------------------------------
    # ---Na kraj otpechatete gi poziciite na shatorite-----


