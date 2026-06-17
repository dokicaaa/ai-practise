import pygad  

def read_input():  
    M, N = map(int, input().split())  
    K = int(input())  
    B = int(input())  
  
    unusable = set()  
    for _ in range(B):  
        r, c = map(int, input().split())  
        unusable.add((r, c))  
  
    return M, N, K, unusable  
  
  
def fitness_func(ga_instance, solution, solution_idx):
    # Ги земаме глобалните променливи за да ги користиме
    global M, N, K, unusable
    
    # solution е 1D низа од 0 и 1. Го пресметуваме вкупниот број на поставени прскалки
    num_sprinklers = sum(solution)
    
    # ТРИК: Казнување (Penalty). Ако се поставени повеќе од K прскалки, 
    # решението е невалидно. Враќаме огромен негативен број за да го "убиеме" овој хромозом.
    if num_sprinklers > K:
        return -999999
    
    # Ni treba nachin za sledneje na onie koi se watterd i onie koi se destroyed
    # okolu water
    watered = set()
    destroyed = set()
    
    # Niza os site kordinati okolu placed sprinkle
    offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1),
        (-2, 0),  (2, 0),  (0, -2),  (0, 2)
    ]
   
    for idx, val in enumerate(solution):
        if val == 1:
            row = idx // N
            col = idx % N
            
            if(r, c) not in unusable:
                destroyed.add((row, col))
                
        # Seag odime niz offset nizata i pravime novi coridinati
        for dr, dc in offsets:
            nr, nc = row + dr, col + dc
            
            # Ako ovie kordinati se vo bounds togash gi dodavame vo waterd
            if 0 <= nr < M and 0 <= nc <= N:
                watered.add((nr, nc ))
    
    # Vistinski validni se onie site navodeni - unsuable i destroyed
    valid_watered = watered - unusable - destroyed
    
    # Tie braker - > ako pokveje ima so so ist broj na watered mora da 
    # go penzliraima toj sto ima povekje
    fitness = len(valid_watered) * 1000 - num_sprinklers
    return fitness
        
# ke imame NxM genoci i sekoj gen mozhe da ima binarna vrednost 0 1 - dali e navodenat i li ne e 
# [0, 1, 0, 0, 0, 0, 1, 0, 0] - Ova e tipicno reshenie
  
#   Genot ima forma [x,y]
if __name__ == "__main__":  
    M, N, K, unusable = read_input()  

    params = {  
        'num_generations': 100,  
        'sol_per_pop': 50,  
        'num_parents_mating': 20,  
        'num_genes': M * N,  # TODO: fill empty params  
        'gene_space': [0,1],  
        'fitness_func': fitness_func,  
        'mutation_num_genes': 1  
    }  
  
    ga = pygad.GA(**params)  
    ga.run()  
  
    best_solution, best_solution_fitness, _ = ga.best_solution()
  
    ...  # TODO: Print required data
    # treba da ispecatime sekoja cordinata na site sprinklers
    sprinkler_positions = []
    for idx, val in enumerate(best_solution):
        if val == 1:
            row = idx // N
            col = idx % N
            sprinkler_positions.append((row,col))
    
    watered_count = int(best_solution_fitness + len(sprinkler_positions)) // 1000
    
    # Печатење на бараниот излез
    print(watered_count)
    print(len(sprinkler_positions))
    for pos in sprinkler_positions:
        print(f"{pos[0]} {pos[1]}")
        
        
        
        
        
    
    