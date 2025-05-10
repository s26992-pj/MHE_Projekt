import random
import sys
from collections import deque
sys.path.append('..')
from Core.generateNeighbours import generate_neighbors
from Core.cel import funkcjaCelu


def tabu_search(numbers, target_sum, tabu_size=5, max_iter=1000, track_convergence=None, epsilon=0.00001):
    current = random.sample(numbers, k=random.randint(1, len(numbers)))
    best = current[:]
    best_score = funkcjaCelu(best, target_sum)

    if tabu_size is None or tabu_size == 0:
        tabu_list = deque()
    else:
        tabu_list = deque(maxlen=tabu_size)
    history_stack = []

    if track_convergence is None:
        track_convergence = []

    for iteration in range(max_iter):
        neighbors = generate_neighbors(current, numbers)
        neighbors = [n for n in neighbors if n not in tabu_list]

        if not neighbors:
            # Brak dostępnych sąsiadów
            if history_stack:
                # Cofnij się do ostatniego punktu roboczego
                current = history_stack.pop()
                print(f"Brak nowych sąsiadów, cofam się do poprzedniego rozwiązania: {current}")
                continue
            else:
                print("Brak dostępnych sąsiadów i brak historii — koniec.")
                break

        # Wybierz najlepszego sąsiada
        next_solution = max(neighbors, key=lambda x: funkcjaCelu(x, target_sum))
        history_stack.append(current)
        current = next_solution

        score = funkcjaCelu(current, target_sum)
        if score > best_score:
            best = current
            best_score = score

        tabu_list.append(current)

        diff = abs(sum(current) - target_sum)
        track_convergence.append(diff)

        print(f"Iteracja {iteration + 1}: Rozwiązanie {current}, Cel: {score}, Różnica: {diff}")

        # Jeśli różnica jest wystarczająco mała (mniejsza niż epsilon), zakończ algorytm
        if diff < epsilon:
            print("Znaleziono rozwiązanie bliskie idealnemu!")
            break

    print("\nNajlepsze znalezione rozwiązanie:", best)
    print("Suma:", sum(best))
    print("Różnica od celu:", abs(sum(best) - target_sum))

    return best, sum(best), abs(sum(best) - target_sum), track_convergence
