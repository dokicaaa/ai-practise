from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())

    # Add the domains
    problem.addVariable("Marija_attendance", [0, 1])
    problem.addVariable("Simona_attendance", [0, 1])
    problem.addVariable("Petar_attendance", [0, 1])
    problem.addVariable("time_meeting", range(12, 20))
    # ----------------------------------------------------

    # ---Add the constraints----------------
    # 1. Simona must attend
    problem.addConstraint(
        lambda s: s == 1,
        ["Simona_attendance"]
    )

    # 2 Simona must attend with atleast one person
    problem.addConstraint(
        lambda m,p: m + p >= 1,
        ["Marija_attendance", "Petar_attendance"]
    )

    # 3. Simona available
    problem.addConstraint(
        lambda s,t: s == 0 or t in {13, 14, 16, 19},
        ["Simona_attendance", "time_meeting"]
    )

    # 3.Maria available
    problem.addConstraint(
        lambda m, t: m == 0 or t in {14, 15, 18},
        ["Marija_attendance", "time_meeting"]
    )

    problem.addConstraint(
        lambda p, t: p == 0 or t in {12, 13, 16, 17, 18, 19},
        ["Petar_attendance", "time_meeting"]
    )
    [print(solution) for solution in problem.getSolutions()]
