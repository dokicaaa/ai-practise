from constraint import *

if __name__ == '__main__':
    problem = Problem(BacktrackingSolver())

    movies = dict()

    n = int(input())
    for _ in range(n):
        film_info = input()
        film, genre, time = film_info.split(' ')
        movies[film] = (float(time), genre)

    l_days = int(input())

    # Tuka definirajte gi promenlivite i domenite
    film_ids = list(movies.keys())

    for film in film_ids:
        problem.addVariable(f"{film}_day", list(range(1, l_days + 1)))
        problem.addVariable(f"{film}_time", list(range(12, 24)))
        problem.addVariable(f"{film}_cinema", [1, 2])

    # Tuka dodadete gi ogranichuvanjata
    # 1.Horror films start >21
    for film, (duration, genre) in movies.items():
        if genre == "horror":
            problem.addConstraint(
                lambda t: t >= 21,
                [f"{film}_time"]
            )

    # 2.Site filmovi koi se pomalku id 2 saati da se prikazhani vo ist den
    short_films = []
    for film, info in movies.items():
        if info[0] <= 2:
            short_films.append(film)

    if len(short_films) > 1:
        problem.addConstraint(
            AllEqualConstraint(),
            [f"{film}_day" for film in short_films]
        )

    # 3. No films can overlap
    def no_overlap(day1, time1, cinema1, day2, time2, cinema2, dur1, dur2):
        if day1 != day2 or cinema1 != cinema2:
            return True

        end1 = time1+dur1
        end2 = time2+dur2
        return end1 <= time2 or end2 <= time1


    for film, (duration, genre) in movies.items():
        problem.addConstraint(
            lambda t, dur=duration: t + dur <= 24,
            [f"{film}_time"]
        )

    for i in range(len(film_ids)):
        for j in range(i+1, len(film_ids)):
            f1, f2 = film_ids[i], film_ids[j]
            dur1, dur2 = movies[f1][0], movies[f2][0]
            problem.addConstraint(
                lambda d1, t1, c1, d2, t2, c2, du1=dur1, du2=dur2:
                no_overlap(d1, t1, c1, d2, t2, c2, du1, du2),
                [f"{f1}_day", f"{f1}_time", f"{f1}_cinema",
                 f"{f2}_day", f"{f2}_time", f"{f2}_cinema"]
            )


    result = problem.getSolution()

    # Tuka dodadete go kodot za pechatenje

    if result is None:
        print("No Solution!")
    else:
        for film in film_ids:
            day = result[f"{film}_day"]
            time = result[f"{film}_time"]
            cinema = result[f"{film}_cinema"]
            print(f"{film}: Day {day} {time}:00 - Cinema {cinema}")