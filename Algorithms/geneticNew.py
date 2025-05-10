import random
import sys

sys.path.append('..')
from Core.cel import funkcjaCeluMapowana

# Inicjalizacja populacji (binarnie)
def initialize_population(numbers, size):
    population = []
    for _ in range(size):
        genotype = [random.randint(0, 1) for _ in range(len(numbers))]
        population.append(genotype)
    return population


# Krzyżowanie jednopunktowe
def one_point_crossover(p1, p2):
    if len(p1) <= 1:
        return p1[:], p2[:]
    cut = random.randint(1, len(p1) - 1)
    return p1[:cut] + p2[cut:], p2[:cut] + p1[cut:]


# Krzyżowanie uniform
def uniform_crossover(p1, p2):
    child1, child2 = [], []
    for a, b in zip(p1, p2):
        child1.append(a if random.random() < 0.5 else b)
        child2.append(b if random.random() < 0.5 else a)
    return child1, child2


# Mutacja typu flip (0 ↔ 1)
def mutate_flip(genotype, mutation_rate=0.6):
    mutated = genotype[:]
    for i in range(len(mutated)):
        if random.random() < mutation_rate:
            mutated[i] = 1 - mutated[i]
    return mutated


# Selekcja turniejowa
def select_parents(population, numbers, target, tournament_size=5):
    tournament = random.sample(population, tournament_size)
    sorted_tournament = sorted(
        tournament, key=lambda x: funkcjaCeluMapowana(x, numbers, target), reverse=True
    )
    return sorted_tournament[:2]


# Główna funkcja algorytmu genetycznego
def genetic_algorithm_new(numbers, target_sum, pop_size=20, max_generations=100,
                      mutation_rate=0.05, crossover_method='one_point',
                      stopping_condition='no_improve', max_no_improve=20,
                      use_elite=True, track_convergence=None):

    population = initialize_population(numbers, pop_size)
    best = max(population, key=lambda x: funkcjaCeluMapowana(x, numbers, target_sum))
    best_score = funkcjaCeluMapowana(best, numbers, target_sum)
    best_gen = 0
    generations_no_improve = 0

    for generation in range(max_generations):
        new_population = []
        if use_elite:
            new_population.append(best[:])  # zachowujemy najlepszego

        while len(new_population) < pop_size:
            parent1, parent2 = select_parents(population, numbers, target_sum)

            if crossover_method == 'one_point':
                child1, child2 = one_point_crossover(parent1, parent2)
            elif crossover_method == 'uniform':
                child1, child2 = uniform_crossover(parent1, parent2)
            else:
                raise ValueError("Nieznana metoda krzyżowania")

            child1 = mutate_flip(child1, mutation_rate)
            child2 = mutate_flip(child2, mutation_rate)

            new_population.extend([child1, child2])

        population = new_population[:pop_size]
        current_best = max(population, key=lambda x: funkcjaCeluMapowana(x, numbers, target_sum))
        current_score = funkcjaCeluMapowana(current_best, numbers, target_sum)

        selected = [num for bit, num in zip(current_best, numbers) if bit == 1]

        print(f"Pokolenie {generation+1:3}, wynik: {current_score:5.2f}, "
              f"suma: {sum(selected):3}, różnica: {abs(sum(selected) - target_sum):3}, "
              f"zbiór: {selected}")

        if current_score > best_score:
            best_score = current_score
            best = current_best[:]
            best_gen = generation + 1
            generations_no_improve = 0
        else:
            generations_no_improve += 1

        if track_convergence is not None:
            track_convergence.append(abs(sum(selected) - target_sum))

        if stopping_condition == 'no_improve' and generations_no_improve >= max_no_improve:
            print("Stop: brak poprawy")
            break
        elif stopping_condition == 'generations' and generation >= max_generations - 1:
            print("Stop: limit pokoleń")
            break

    best_selected = [num for bit, num in zip(best, numbers) if bit == 1]

    print("\nNajlepsze rozwiązanie:")
    print(f"Zbiór: {best_selected}")
    print(f"Suma: {sum(best_selected)}, Różnica: {abs(sum(best_selected) - target_sum)}")
    print(f"Pokolenie: {best_gen}")
    print(f"binary: {population}")

    return best, track_convergence
