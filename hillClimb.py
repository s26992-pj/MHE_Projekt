import sys
import random
sys.path.append('..')
from Core.generateNeighbours import generate_neighbors
from Core.cel import funkcjaCelu


def hill_climb_best(numbers, target_sum, max_iterations=1000):
    current = random.sample(numbers, random.randint(1, len(numbers)))
    current_score = funkcjaCelu(current, target_sum)

    convergence = []

    for _ in range(max_iterations):
        neighbors = generate_neighbors(current, numbers)
        if not neighbors:
            break

        best_neighbor = max(neighbors, key=lambda x: funkcjaCelu(x, target_sum))
        best_score = funkcjaCelu(best_neighbor, target_sum)

        if best_score > current_score:
            current = best_neighbor
            current_score = best_score
        else:
            break

    convergence.append(abs(sum(current) - target_sum))
    return current, sum(current), abs(sum(current) - target_sum), convergence


def hill_climb_random(numbers, target_sum, max_iterations=1000):
    current = random.sample(numbers, random.randint(1, len(numbers)))
    current_score = funkcjaCelu(current, target_sum)

    convergence = []
    for _ in range(max_iterations):
        neighbors = generate_neighbors(current, numbers)
        if not neighbors:
            break

        candidate = random.choice(neighbors)
        candidate_score = funkcjaCelu(candidate, target_sum)

        if candidate_score > current_score:
            current = candidate
            current_score = candidate_score

    convergence.append(abs(sum(current) - target_sum))
    return current, sum(current), abs(sum(current) - target_sum), convergence
