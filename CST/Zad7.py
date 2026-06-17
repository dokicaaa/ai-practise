from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())
    # --- ПРОМЕНИ ГО ОВОЈ ДЕЛ ---
    lecture_slots_AI = int(input().strip())
    lecture_slots_ML = int(input().strip())
    lecture_slots_R = int(input().strip())
    lecture_slots_BI = int(input().strip())
    AI_lectures_domain = ["Mon_11", "Mon_12", "Wed_11", "Wed_12", "Fri_11", "Fri_12"]
    ML_lectures_domain = ["Mon_12", "Mon_13", "Mon_15", "Wed_12", "Wed_13", "Wed_15", "Fri_11", "Fri_12", "Fri_15"]
    R_lectures_domain = ["Mon_10", "Mon_11", "Mon_12", "Mon_13", "Mon_14", "Mon_15", "Wed_10", "Wed_11", "Wed_12",
                         "Wed_13", "Wed_14", "Wed_15", "Fri_10", "Fri_11", "Fri_12", "Fri_13", "Fri_14", "Fri_15"]
    BI_lectures_domain = ["Mon_10", "Mon_11", "Wed_10", "Wed_11", "Fri_10", "Fri_11"]

    AI_exercises_domain = ["Tue_10", "Tue_11", "Tue_12", "Tue_13", "Thu_10", "Thu_11", "Thu_12", "Thu_13"]
    ML_exercises_domain = ["Tue_11", "Tue_13", "Tue_14", "Thu_11", "Thu_13", "Thu_14"]
    BI_exercises_domain = ["Tue_10", "Tue_11", "Thu_10", "Thu_11"]

    # ---Add the variables here--------------------
    # Niza za site proemniliviv na kraj
    all_variables=[]

    ai_lectures = [f"AI_lecture_{i + 1}" for i in range(lecture_slots_AI)]
    problem.addVariables(ai_lectures, AI_lectures_domain)
    problem.addVariable("AI_exercises", AI_exercises_domain)
    all_variables.extend(ai_lectures + ["AI_exercises"])

    # 2. Machine Learning (ML)
    ml_lectures = [f"ML_lecture_{i + 1}" for i in range(lecture_slots_ML)]
    problem.addVariables(ml_lectures, ML_lectures_domain)
    problem.addVariable("ML_exercises", ML_exercises_domain)
    ml_all = ml_lectures + ["ML_exercises"]  # Ги чуваме посебно за условот за ML
    all_variables.extend(ml_all)

    # 3. Robotics (R) - Нема вежби
    r_lectures = [f"R_lecture_{i + 1}" for i in range(lecture_slots_R)]
    problem.addVariables(r_lectures, R_lectures_domain)
    all_variables.extend(r_lectures)

    # 4. Bioinformatics (BI)
    bi_lectures = [f"BI_lecture_{i + 1}" for i in range(lecture_slots_BI)]
    problem.addVariables(bi_lectures, BI_lectures_domain)
    problem.addVariable("BI_exercises", BI_exercises_domain)
    all_variables.extend(bi_lectures + ["BI_exercises"])

    # ---Add the constraints here----------------
    # 1. Ne smee da ima preklopuvanje na terminite
    # Start hour - End Hour - abs(hour1 - hour2 ) < 2 - False
    def no_overlap(time1, time2):
        day1, hour1 = time1.split('_')
        day2, hour2 = time2.split('_')

        # Ako se isti den
        if day1 == day2:
            if abs(int(hour1) - int(hour2)) < 2:
                return False
        return True

    # Sega za da ja koristime funkcijava mora za sekohj mozhen par od variables da go napravime
    for i in range(len(all_variables)):
        for j in range(i + 1, len(all_variables)):
            problem.addConstraint(no_overlap, [all_variables[i], all_variables[j]])

    # 2. Perdavanja Vezbie za ML mora da pocnuvaata sekoj den vo razlivno vreme. ne smee razlicni denovi isto vreme
    def ml_different_hours(*ml_times):
        # Treba da gi izvadime saatte od sekoj guess na solverot *ml_times - ova znaci deka samo go prakjash arguemntot kako torka
        hours = [time.split('_')[1] for time in ml_times]

        # Кога Python ќе ја види листата ['12', '12', '13'], тој безмилосно го брише вториот број '12'.
        # Множеството сега станува: {'12', '13'}. AKO SE ISTA GOLEMNA TOGASHB NEMA DUPLIKATI
        return len(hours) == len(set(hours))

    problem.addConstraint(ml_different_hours, ml_all)

    # ----------------------------------------------------
    solution = problem.getSolution()

    print(solution)