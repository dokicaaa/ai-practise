from constraint import *

# Sudoku tabla - 9 Kocki so 9 vnatresni- toa e 81
# 81 variables sekoja so vrednost 1-9
if __name__ == '__main__':
    type = input().strip()
    
    if type == "BacktrackingSolver":
        solver = BacktrackingSolver()
    elif type == "RecursiveBacktrackingSolver":
        solver = RecursiveBacktrackingSolver()
    else:
        solver = MinConflictsSolver()
    
    problem = Problem(solver)

    # Define varibales
    for i in range(81):
        problem.addVariable(i, Domain(set(range(1, 10))))
    
    # -------------CONTSTRAINTS --------------  
      
    # AllDiff za redica
    for r in range(9):
        # Since it is a 1d array, we need to think to multiple r by 9 
        # since there are 9 cols in each row R * N + C
        row_cells = [r * 9 + c for c in range(9)]
        problem.addConstraint(AllDifferentConstraint(), row_cells)
    
    # Alldif za kolona
    for c in range(9):
        col_cells = [r * 9 + c for r in range(9)]
        problem.addConstraint(AllDifferentConstraint(), col_cells)
    
    # Alldiff za sekoj 3x3 blok
    for block_row in range(3):  # OUTER BIG BLOCK ROWS OF 3
        for block_col in range(3): #OUTER BIG BLOCK COLS OF 3
            # Niza za translating indeksi vo 1 block
            block_cells = []
            for r in range(3):
                for c in range(3):
                    # Absolute Row = (block_row * 3 + r)
                    # Absolute Column = (block_column * 3 + c)
                    # Index = (Absolute Row) * 9 + (Absolute Column)
                    cell = (block_row * 3 + r) * 9 + (block_col * 3 + c)
                    block_cells.append(cell)

            problem.addConstraint(AllDifferentConstraint(), block_cells)   
    
    print(problem.getSolution())    
            
            