from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())
    variables = ["A", "B", "C", "D", "E", "F"]
    for variable in variables:
        problem.addVariable(variable, Domain(set(range(101))))

    # ---Tuka dodadete gi ogranichuvanjata----------------
    # 1. Site se razlicni, AllDifferentConstraint
    problem.addConstraint(AllDifferentConstraint(), variables)

    # 2. B D E mora da se odd - not built in
    for var in ["B", "D", "E"]:
        problem.addConstraint(lambda x: x % 2 != 0, [var])

    # 3. A B C MaxSumConstraint
    problem.addConstraint(MinSumConstraint(100), ["A", "B", "C"])
    # 4. D E ExactSumConstraint
    problem.addConstraint(ExactSumConstraint(150), ["D", "E"])
    # 5. F Edinci delivi so 2
    problem.addConstraint(lambda F: (F % 10) % 4 == 0, ["F"])

    # ----------------------------------------------------

    print(problem.getSolution())