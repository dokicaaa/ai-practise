from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())
    variables = ["S", "E", "N", "D", "M", "O", "R", "Y"]
    for variable in variables:
        problem.addVariable(variable, Domain(set(range(10))))

#Sekoja bukva pretstavuav eden boroj 0-9
# Constraints: dve bukvi ne mozhe isatat cifra, ako bukvata se povtoruva, togash ista cifra

    # 1. All leters represent diff digit
    problem.addConstraint(AllDifferentConstraint(), variables)

    # 2.Mora aritmetickata da e tocna
    problem.addConstraint(
        lambda S, E, N, D, M, O, R, Y:
        (1000 * S + 100 * E + 10 * N + D) +
        (1000 * M + 100 * O + 10 * R + E) ==
        (10000 * M + 1000 * O + 100 * N + 10 * E + Y),
        ["S", "E", "N", "D", "M", "O", "R", "Y"]
    )
    # 3. Brojot ne smee da pocne so 0
    problem.addConstraint(lambda S: S != 0, ["S"])
    problem.addConstraint(lambda M: M != 0, ["M"])
    print(problem.getSolution())