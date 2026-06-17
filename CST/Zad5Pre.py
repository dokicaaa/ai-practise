from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())

    # Add the domains
    problem.addVariable("Marija_attendance", [0, 1])
    problem.addVariable("Simona_attendance", [0, 1])
    problem.addVariable("Petar_attendance", [0, 1])
    problem.addVariable("time_meeting", range(12, 20))
    # ----------------------------------------------------

    # Lista za site mozni vreminaj za sekoj chovek -> posle ke go koristme ova za in set contraint
    simona_times = [13, 14, 16, 19]
    marija_times = [14, 15, 18]
    petar_times = [12, 13, 16, 17, 18, 19]

    # ---Add the constraints----------------
    # 1.Simona must attend all meetings
    problem.addConstraint(InSetConstraint([1]), ["Simona_attendance"])

    # 2. Simona mora da bide so minimum 1 chovek
    # SomeInSetConstraint so par 1 proveruav dali barem eden od listat na vars e vo nizata
    problem.addConstraint(SomeInSetConstraint([1]), ["Marija_attendance", "Petar_attendance"])

    # 3.Vremeto na sostanocite mora da e vo available times na simona
    problem.addConstraint(InSetConstraint(simona_times), ["time_meeting"])

    # 4. Ako marija prisustvuva mora da e vo nejzini termini
    # Ako marija ne prisustuvva ili ako vremeto se sofpagja togash vrakja true
    problem.addConstraint(lambda m, t: m == 0 or t in marija_times, ["Marija_attendance", "time_meeting"])

    # Isto i za petar
    problem.addConstraint(lambda p,t: p == 0 or t in petar_times, ["Petar_attendance", "time_meeting"])

    # ----------------------------------------------------
    solutions = problem.getSolutions()

    # We must order them corfrectly so it prints good
    solutions = problem.getSolutions()

    # Define the exact order the auto-grader wants
    ordered_keys = ['Simona_attendance', 'Marija_attendance', 'Petar_attendance', 'time_meeting']

    for solution in solutions:
        # Reconstruct the dictionary in the strict order
        formatted_solution = {key: solution[key] for key in ordered_keys}
        print(formatted_solution)