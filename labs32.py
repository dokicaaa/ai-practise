from constraint import Problem, BacktrackingSolver
def read_input():
    num_families = int(input())
    families = {}
    for _ in range(num_families):
        name, size, reqs_string = input().split()
        reqs = reqs_string.split('-')
        families[name] = {'size': int(size), 'requirements': reqs}

    num_rooms = int(input())
    rooms = {}
    for _ in range(num_rooms):
        room_id, capacity, amenities_string = input().split()
        floor = room_id[0]
        amenities = amenities_string.split('-')
        rooms[int(room_id)] = {'floor': int(floor), 'capacity': int(capacity), 'amenities': amenities}

    return families, rooms

if __name__ == '__main__':
    problem = Problem(solver=BacktrackingSolver())

    families, rooms = read_input()

    # Dodadete gi promenlivite i domenite tuka.
    # Add the variables and domains here.

    # Site sobi koi zadovoluvaat se stavaat vo listat so vrednost 1, 0 rejected
    room_ids = list(rooms.keys())

    for name, info in families.items():
        valid_rooms = [0]
        for room_id, room_info in rooms.items():
            fits_capacity = room_info['capacity'] >= info['size']
            fits_amenities = all(req in room_info['amenities'] for req in info['requirements'])
            if fits_capacity and fits_amenities:
                valid_rooms.append(room_id)
        problem.addVariable(name, valid_rooms)

    family_names = list(families.keys())

    # Dodadete gi ogranichuvanjata tuka.
    # Add the constraints here.

    #Dve familii da ne se vo ista soba
    for i in range(len(family_names)):
        for j in range(i + 1, len(family_names)):
            problem.addConstraint(
                lambda a, b: a == 0 or b == 0 or a != b,
                [family_names[i], family_names[j]]
            )

    #Da nema odbivanje vez pricina
    # Povekje pati odbieni se dozvoleni
    for name,info in families.items():
        fitting_rooms = [
            room_id for room_id, room_info in rooms.items()
            if room_info['capacity'] >= info['size']
            and all(req in room_info['amenities'] for req in info['requirements'])
        ]
        if not fitting_rooms:
            continue  #Ne mozhat da se stavat vo nikoja soba, rejection always justified

        others = [n for n in family_names if n != name]

        def make_constraint(fitting, fname=name):
            def constraint(*args):
                # args[0]  = assigned room na familija (or 0)
                # args[1:] = assigned rooms na ostanatite familii
                this_room = args[0]
                other_rooms = set(args[1:])
                if this_room == 0:
                    for fr in fitting:
                        if fr not in other_rooms:
                            return False  # ako ima soba koja moze da odgovara - unjustified rejection
                return True

            return constraint


        problem.addConstraint(make_constraint(fitting_rooms), [name] + others)

    solutions = problem.getSolutions()  # Ne menuvaj! Do not modify!

    # Ispechatete go najdobroto reshenie vo baraniot format.
    # Print the best solution in the required format.

    #Najdobar = mak total broj na lugje so dobiena soba
    def total_people(sol):
        return sum(
            families[name]['size']
            for name, room in sol.items()
            if room != 0
        )

    if not solutions:
        print("No solution found")
    else:
        best = max(solutions, key=total_people)

        # Soberi assigned rooms i sortiraj spored broj
        assigned = {room: name for name, room in best.items() if room != 0}

        print("Best assignment:")
        for room_id in sorted(assigned.keys()):
            print(f"{assigned[room_id]}->{room_id}")
