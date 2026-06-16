from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())
    
    variables = ["A", "B", "C", "D", "E", "F"]
    for var in variables:
        problem.addVariable(var, Domain(set(range(100))))
    # ---Tuka dodadete gi ogranichuvanjata----------------
    
    # 1. Ne postojat var koi imaat ista vrednost
    problem.addConstraint(AllDifferentConstraint(), variables)
    
    # 2.Var B D E treba da imaat neparni vrednost
    for var in ["B", "D", "E"]:
        problem.addConstraint(lambda x: x % 2 != 0, [var])
        
    # the lamba id a on line fucntion in mython - this is the same.
    # def is_odd(x):
    # return x % 2 != 0

    # for var in ['B', 'D', 'E']:
    # problem.addConstraint(is_odd, [var])
    
    # 3. Zbirot na A B i C ne smee da e pomal od 100
    problem.addConstraint(MinSumConstraint(100), ["A","B", "C" ] )
    
    # 4. D E mora da e tocno 150
    problem.addConstraint(ExactSumConstraint(150), ["D","E"] )
    
    # 5. F must have a digit which is devidable by 4
    problem.addConstraint(lambda F: (F % 10) % 4 == 0, ["F"])
    

    # ----------------------------------------------------
    
    print(problem.getSolution())