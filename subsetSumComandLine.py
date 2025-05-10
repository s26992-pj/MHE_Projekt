import argparse
import sys
from Core.cel import funkcjaCelu
from Core.randomSolution import randomSolution
from Core.loadData import loadData
from Core.generateNeighbours import generate_neighbors
from Algorithms.bruteForce import brute_force
from Algorithms.hillClimb import hill_climb_best, hill_climb_random
from Algorithms.simulatedAnnealing import simulated_annealing
from Algorithms.tabu import tabu_search
from Algorithms.genetic import genetic_algorithm


#Implementacja Problemu
def run_Basic(file, target):
    data = loadData(file)
    rand = randomSolution(data)
    obj = funkcjaCelu(rand, target)
    neigh = generate_neighbors(rand, data)

    print(f"Losowe rozwiązanie: {rand} (wartość celu: {obj})")
    print("Przykładowi sąsiedzi:")
    for n in neigh[:5]:
        print(n)


def run_bruteforce(file, target):
    data = loadData(file)
    bestSubset, sumSubset = brute_force(data, target)
    print("Najlepszy pasujący podzbiór:", bestSubset)
    print("Suma:", sumSubset)
    print("Różnica od celu:", abs(sumSubset - target))


def run_genetic(file, target, pop, cross, mut, stop, elite):
    numbers = loadData(file)
    genetic_algorithm(
        numbers=numbers,
        target_sum=target,
        pop_size=pop,
        crossover_method=cross,
        mutation_method=mut,
        stopping_condition=stop,
        use_elite=elite
    )


def run_hillclimb(file, target, mode):
    data = loadData(file)
    if mode == "best":
        result, total, diff = hill_climb_best(data, target)
    elif mode == "random":
        result, total, diff = hill_climb_random(data, target)
    else:
        print("Nieznany tryb hill climbing. Wybierz 'best' lub 'random'.")
        return
    print("Najlepszy znaleziony podzbiór:", result)
    print("Suma podzbioru:", total)
    print("Różnica od celu:", diff)


def run_simulated(file, target, schedule, alpha):
    if not schedule or alpha is None:
        print("Dla simulated annealing wymagane są --schedule i --alpha")
        sys.exit(1)
    data = loadData(file)
    simulated_annealing(data, target, schedule=schedule, alpha=alpha)


def run_tabu(file, target, tabu_size):
    if tabu_size is None:
        print("Dla tabu wymagane jest --size")
        sys.exit(1)
    data = loadData(file)
    tabu_search(data, target, tabu_size)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Algorytmy optymalizacji dla problemu podzbiorów.")
    parser.add_argument("algorithm", type=str, choices=["base", "bruteforce", "genetic", "hillclimb", "simulated", "tabu"], help="Wybierz algorytm")
    parser.add_argument("--file", required=True, help="Plik wejściowy z liczbami")
    parser.add_argument("--target", type=int, required=True, help="Suma docelowa")

    # Argumenty specyficzne Genetyczny
    parser.add_argument("--pop", type=int, default=50, help="Rozmiar populacji (genetic)")
    parser.add_argument("--cross", type=str, choices=["one_point", "uniform"], default="one_point", help="Metoda krzyżowania")
    parser.add_argument("--mut", type=str, choices=["add_remove", "swap"], default="add_remove", help="Metoda mutacji")
    parser.add_argument("--stop", type=str, choices=["no_improve", "generations"], default="generations", help="Warunek stopu")
    parser.add_argument("--elite", type=int, choices=[0, 1], default=1, help="Czy używać elity")
    parser.add_argument("--generations", type=int, default=100, help="Maksymalna liczba pokoleń")
    parser.add_argument("--mrate", type=float, default=0.6, help="Współczynnik mutacji")

    # Argumenty specyficzne hill climbing
    parser.add_argument("--mode", type=str, choices=["best", "random"], help="Tryb dla hill climbing")

    # Argumenty specyficzne simulated annealing
    parser.add_argument("--schedule", type=str, choices=["linear", "exponential", "logarithmic"], help="Typ schematu")
    parser.add_argument("--alpha", type=float, help="Współczynnik schładzania")

    # Argumenty specyficzne Tabu
    parser.add_argument("--size", type=int, help="Rozmiar Tabu")
    args = parser.parse_args()

    if args.algorithm == "base":
        run_Basic(args.file, args.target)
    elif args.algorithm == "bruteforce":
        run_bruteforce(args.file, args.target)
    elif args.algorithm == "genetic":
        run_genetic(args.file, args.target, args.pop, args.cross, args.mut, args.stop, bool(args.elite))
    elif args.algorithm == "simulated":
        run_simulated(args.file, args.target, args.schedule, args.alpha)
    elif args.algorithm == "tabu":
        run_tabu(args.file, args.target, args.size)
    elif args.algorithm == "hillclimb":
        if not args.mode:
            print("podaj --mode dla hillclimb (best/random)")
            sys.exit(1)
        run_hillclimb(args.file, args.target, args.mode)

