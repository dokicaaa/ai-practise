from constraint import *

if __name__ == '__main__':

    bands = dict()

    band_info = input()
    while band_info != 'end':
        band, genre, time = band_info.split(' ')
        bands[band] = (genre, time)
        band_info = input()

    # Add the variables here
    # Variabli se dcit Band od 1 do 10: (genre, time) so domen s1,s2,s3
    variables = list(bands.keys())

    domain = [f'S{i + 1}' for i in range(3)]

    problem = Problem(BacktrackingSolver())
    problem.addVariables(variables, domain)

    # SEKOJA BINA 1 Nastap od 120 minuti, namnogu 5 benodvi sto svirat <80 min
    bands_120 = [band for band,data in bands.items() if int(data[1]) == 120]
    problem.addConstraint(AllDifferentConstraint(), bands_120)

    bands_under_80 = [b for b, data in bands.items() if int(data[1]) < 80]
    # za sekoj stage ako countott za sekoj bend od 60 ili 8 e pogolem od 5 togash e false
    def max_5_80(*args):
        for stage in domain:
            if args.count(stage) > 5:
                return False
        return True

    problem.addConstraint(max_5_80, bands_under_80)

    for genre in ["punk", "metal", "rock"]:
        bands_in_genre = [band for band, data in bands.items() if data[0] == genre]
        total_time = sum(int(data[1]) for b, data in bands.items() if data[0] == genre)

        if total_time <= 300:
            problem.addConstraint(AllEqualConstraint(), bands_in_genre)


    result = problem.getSolution()

    # Add the printing section here
    if result:
        # ✅ Correct printing
        for band in bands:
            print(f"{band} ({bands[band]}): {result[band]}")