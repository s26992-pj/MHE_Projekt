import math
import random
import sys
sys.path.append('..')
from Core.generateNeighbours import generate_neighbors
from Core.cel import funkcjaCelu


def cooling_schedule(temp, alpha, schedule_type, iteration):
    if schedule_type == "linear":
        return temp - alpha
    elif schedule_type == "exponential":
        return temp * alpha
    elif schedule_type == "logarithmic":
        return temp / (1 + alpha * math.log(1 + iteration))
    else:
        raise ValueError("Nieznany typ schematu: " + schedule_type)


def simulated_annealing(numbers, target_sum, initial_temp=100, alpha=0.95, schedule="exponential", max_iter=1000, track_convergence=None):

    current = random.sample(numbers, k=random.randint(1, len(numbers)))
    best = current[:]
    best_score = funkcjaCelu(best, target_sum)
    temperature = initial_temp

    if track_convergence is None:
        track_convergence = []

    for i in range(max_iter):
        neighbors = generate_neighbors(current, numbers)
        neighbor = random.choice(neighbors)
        delta = funkcjaCelu(neighbor, target_sum) - funkcjaCelu(current, target_sum)

        if delta > 0 or random.random() < math.exp(delta / temperature):
            current = neighbor

        if funkcjaCelu(current, target_sum) > best_score:
            best = current[:]
            best_score = funkcjaCelu(best, target_sum)

        diff_to_target = abs(sum(current) - target_sum)
        track_convergence.append(diff_to_target)
        print(f"Iteracja {i+1}, Temp: {temperature:.2f}, Cel: {funkcjaCelu(current, target_sum)}, Rozwiązanie: {current}")

        temperature = cooling_schedule(temperature, alpha, schedule, i + 1)
        if temperature <= 0.0001:
            break

    print("\nNajlepsze rozwiązanie:", best)
    print("Suma:", sum(best))
    print("Różnica od celu:", abs(sum(best) - target_sum))

    return best, sum(best), abs(sum(best) - target_sum), track_convergence