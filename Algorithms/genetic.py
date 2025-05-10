import random
import sys

sys.path.append('..')
from Core.cel import funkcjaCelu


# Inicjalizacja populacji
def initialize_population(numbers, size, target_sum):
    population = []

    while len(population) < size:
        # Zapewniamy, że rozmiar próbki będzie w granicach dostępnych liczb
        count = random.randint(1, len(numbers))
        individual = random.sample(numbers, count)
        population.append(individual)

    return population


# Krzyżowanie jednopunktowe
def one_point_crossover(p1, p2):
    #ustaw 1 jeżeli jeden z rodziców ma jeden elemt
    if len(p1) <= 1 or len(p2) <= 1:
        cut = 1
    else:
        cut = random.randint(1, min(len(p1), len(p2)) - 1)

    child1 = p1[:cut] + p2[:cut]
    child2 = p2[:cut] + p1[:cut]

    return child1, child2


# Krzyżowanie uniform
def uniform_crossover(p1, p2):
    child1, child2 = [], []
    for a, b in zip(p1, p2):
        if random.random() < 0.5:
            child1.append(a)
        else:
            child1.append(b)
        if random.random() < 0.5:
            child2.append(a)
        else:
            child2.append(b)
    return child1, child2


# Mutacja typu add/remove
def mutate_add_remove(solution, all_numbers, mutation_rate=0.6):
    solution = solution[:]
    if random.random() < mutation_rate and len(solution) > 1:
        solution.pop(random.randint(0, len(solution) - 1))
    if random.random() < mutation_rate:
        candidates = [x for x in all_numbers if x not in solution]
        if candidates:
            solution.append(random.choice(candidates))
    return solution


# Mutacja typu swap
def mutate_swap(solution, _, mutation_rate=0.6):
    if len(solution) > 1 and random.random() < mutation_rate:
        i, j = random.sample(range(len(solution)), 2)
        solution[i], solution[j] = solution[j], solution[i]
    return solution


# Selekcja turniejowa
def select_parents(population, target, tournament_size=5):
    if len(population) < tournament_size:
        raise ValueError("Population size is smaller than the tournament size.")
    tournament = random.sample(population, tournament_size)
    sorted_tournament = sorted(tournament, key=lambda x: funkcjaCelu(x, target), reverse=True)
    return sorted_tournament[:2]


# Główna funkcja algorytmu
def genetic_algorithm(numbers, target_sum, pop_size=20, max_generations=100, mutation_rate=0.6,
                      crossover_method='one_point', mutation_method='add_remove',
                      stopping_condition='no_improve', max_no_improve=20, use_elite=1,track_convergence=None):

    population = initialize_population(numbers, pop_size, target_sum)
    bestPopulation = 0,
    best = max(population, key=lambda x: funkcjaCelu(x, target_sum))
    best_score = funkcjaCelu(best, target_sum)
    generations_no_improve = 0

    for generation in range(max_generations):
        new_population = []
        if use_elite:
            new_population.append(best[:])

        while len(new_population) < pop_size:
            parent1, parent2 = select_parents(population, target_sum)

            if crossover_method == 'one_point':
                child1, child2 = one_point_crossover(parent1, parent2)
            elif crossover_method == 'uniform':
                child1, child2 = uniform_crossover(parent1, parent2)
            else:
                raise ValueError("Nieznana metoda krzyżowania")

            if mutation_method == 'add_remove':
                child1 = mutate_add_remove(child1, numbers, mutation_rate)
                child2 = mutate_add_remove(child2, numbers, mutation_rate)
            elif mutation_method == 'swap':
                child1 = mutate_swap(child1, numbers, mutation_rate)
                child2 = mutate_swap(child2, numbers, mutation_rate)
            else:
                raise ValueError("Nieznana metoda mutacji")

            new_population.extend([child1, child2])

        population = new_population[:pop_size]
        current_best = max(population, key=lambda x: funkcjaCelu(x, target_sum))
        current_score = funkcjaCelu(current_best, target_sum)

        print(f"Pokolenie {generation+1:3}, najlepszy wynik: {current_score:5},"
              f" suma: {sum(current_best):3},"
              f" różnica: {abs(sum(current_best) - target_sum):3},"
              f" zbiór: {sorted(current_best)}")

        if current_score > best_score:
            best_score = current_score
            best = current_best[:]
            bestPopulation = generation + 1
            generations_no_improve = 0
        else:
            generations_no_improve += 1

        if track_convergence is not None:
            track_convergence.append(abs(sum(current_best) - target_sum))

        if stopping_condition == 'no_improve' and generations_no_improve >= max_no_improve:
            print("Stop: brak poprawy")
            break
        elif stopping_condition == 'generations' and generation >= max_generations - 1:
            print("Stop: limit pokoleń")
            break

    print("\n Najlepsze rozwiązanie:")
    print(f"Zbiór: {sorted(best)}")
    if(bestPopulation) : print(f"poulaton: {bestPopulation}")


    print(f"Suma: {sum(best)}, Różnica: {abs(sum(best) - target_sum)}")

    return best, track_convergence