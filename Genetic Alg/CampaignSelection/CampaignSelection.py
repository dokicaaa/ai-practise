import pygad
import random
random.seed(0)


def read_input():
    N = int(input())
    B = int(input())
    campaigns = []
    for i in range(N):
        cost, profit, channel = input().split()
        campaigns.append({'cost': int(cost), 'profit': int(profit), 'channel': channel})
    return N, B, campaigns

    # Imame lista od poedinecni kampnaji so dictinaries vo nic
    # [{'cost':40 'profit':50 'channel':TV}...]

    # Bidejki pishuva deka treba da se izgberat ke imame N kapanji so domen [0,1]
    # solution -> [0,1, 1 , 0]

def total_profit(solution):
    global N, B, campaigns

    # Treba da imame dictionary so sledi {chanel: num}

    channels_counts = {}
    channels_profits = {}

    for idx, is_selected in enumerate(solution):
        if is_selected == 1:
            ch = campaigns[idx]['channel']
            profit = campaigns[idx]['profit']

            # Zgolemime brojot na kampnaji za sekoj channel
            channels_counts[ch] = channels_counts.get(ch, 0) + 1
            channels_profits[ch] = channels_profits.get(ch, 0) + profit

    total = 0.0

    # Za sekoj kanal od coutns gledame kolku ima, ako ima povekj od tri so istion chanel go zgolemuvame za 1.15
    for ch, count in channels_counts.items():
        if count >= 3:
            total += channels_profits[ch] * 1.15
        else:
            total += channels_profits[ch]

    return total
def fitness_func(ga, solution, solution_idx):

    # treba da presmetame total cost
    total_cost = 0
    for idx, is_selected in enumerate(solution):
        if is_selected == 1:
            total_cost += campaigns[idx]['cost']

    # Tuka go presmetuvame cost cisto za da ja zapazime death peanlty
    if total_cost > B:
        return -99999

    return total_profit(solution)


if __name__ == "__main__":
    N, B, campaigns = read_input()

    params = {
        'num_generations': 500,
        'sol_per_pop': 100,
        'num_parents_mating': 40,
        'num_genes': N,  # TODO
        'gene_space': [0,1],  # TODO
        'fitness_func': fitness_func,
        'mutation_num_genes': 1,
    }

    ga = pygad.GA(**params)
    ga.run()

    best_solution, _ , _ = ga.best_solution(ga.last_generation_fitness)

    ...  # TODO: print total cost, total profit, selected campaigns

    best_profit = total_profit(best_solution)

    best_cost = 0
    for idx, is_selected in enumerate(best_solution):
        if is_selected == 1:
            best_cost += campaigns[idx]['cost']

    print(f"Total cost: {best_cost}")
    print(f"Total profit: {best_profit}")

    for idx, is_selected in enumerate(best_solution):
        if is_selected == 1:
            print(f"Kampanja {idx}: cost={campaigns[idx]['cost']}, profit={campaigns[idx]['profit']}, channel={campaigns[idx]['channel']}")




