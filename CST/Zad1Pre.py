from constraint import *

if __name__ == '__main__':
    # Definirash problem
    problem = Problem(BacktrackingSolver())
    
    # Varibables ke ni se site bukvi okj se naogjaat vo zadacata
    variables = ["S", "E", "N", "D", "M", "O", "R", "Y"]
    
    # Dodavash sekoja variable odn izata vo problemot
    for variable in variables: 
        # OSven toa stavash i koklav e domainot
        problem.addVariable(variable, Domain(set(range(10))))
    
    # ---Tuka dodadete gi ogranichuvanjata----------------
    
    # Tuka stavash contraint deka nikoja variabla vo problem ne smee da e istas
    problem.addConstraint(AllDifferentConstraint(), variables)
    
    # Funkcija za gledanje na zbir na kripotkgrafksata poraka
    # Idea - Od najdesno pocnuvame so 1 i 10, 100, 100 int.
    # Mnozime sekja bukva i ako zbirot e ist so money togash e tocno
    
    def cryptic_check(s, e, n, d, m, o , r, y):
        send = 1000 * s + 100 * e + 10 * n + 1 * d
        more = 1000 * m + 100 * o + 10 * r + 1 * e
        money = 10000 * m + 1000 * o + 100 * n + 10 * e + 1 * y
        
        return send + more == money
    
    problem.addConstraint(cryptic_check, variables)
    
    # ----------------------------------------------------
    
    print(problem.getSolution())