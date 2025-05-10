import argparse
import sys
import time
import psutil
import matplotlib.pyplot as plt
import numpy as np
from Core.loadData import loadData
from Algorithms.bruteForce import brute_force
from Algorithms.hillClimb import hill_climb_best, hill_climb_random
from Algorithms.simulatedAnnealing import simulated_annealing
from Algorithms.tabu import tabu_search
from Algorithms.genetic import genetic_algorithm
from Algorithms.geneticNew import genetic_algorithm_new



# Mierzenie ile bierze zasobów
def measure_performance(func, *args, **kwargs):
    process = psutil.Process()
    initial_memory = process.memory_info().rss / (1024 * 1024)
    start_time = time.time()

    result = func(*args, **kwargs)

    elapsed_time = time.time() - start_time
    final_memory = process.memory_info().rss / (1024 * 1024)
    memory_usage = max(0, final_memory - initial_memory)

    return result, elapsed_time, memory_usage

def run_genetic_new(file, target, pop=50, cross="one_point", mrate=0.05, stop="generations", elite=1, generations=100):
    numbers = loadData(file)
    diffs = []
    best, diffs = genetic_algorithm_new(
        numbers=numbers,
        target_sum=target,
        pop_size=pop,
        max_generations=generations,
        mutation_rate=mrate,
        crossover_method=cross,
        stopping_condition=stop,
        use_elite=bool(elite),
        track_convergence=diffs
    )
    return best, sum(best), abs(sum(best) - target), diffs


# Funkcja Wywołująca BruteForce
def run_bruteforce(file, target):
    data = loadData(file)
    convergence = []
    bestSubset, sumSubset, diff, convergence = brute_force(data, target, track_convergence=convergence)
    return bestSubset, sumSubset, diff, convergence


# Funkcja Wywołująca HillClimb
def run_hillclimb(file, target, mode):
    data = loadData(file)
    if mode == "best":
        result, total, diff, convergence = hill_climb_best(data, target)
    elif mode == "random":
        result, total, diff, convergence = hill_climb_random(data, target)
    else:
        print("Dla hill climbing są tryby 'best' lub 'random'.")
        return None, 0, 0, []
    return result, total, diff, convergence


# Funkcja Wywołująca Simulated Annealing
def run_simulated(file, target, schedule, alpha):
    if not schedule or alpha is None:
        print("Dla simulated annealing wymagane są --schedule i --alpha")
        sys.exit(1)
    data = loadData(file)
    convergence = []
    result = simulated_annealing(data, target, schedule=schedule, alpha=alpha, track_convergence=convergence)
    return result

# Funkcja Wywołująca Tabu Search
def run_tabu(file, target, tabu_size):
    if tabu_size is None:
        print("Dla tabu wymagane jest --size")
        sys.exit(1)
    data = loadData(file)
    convergence = []
    return tabu_search(data, target, tabu_size, track_convergence=convergence)


# Funkcja Wywołująca Genetyczny Algorytm
def run_genetic(file, target, pop, cross, mut, stop, elite):
    numbers = loadData(file)
    diffs = []
    best_individual, diffs = genetic_algorithm(
        numbers=numbers,
        target_sum=target,
        pop_size=pop,
        crossover_method=cross,
        mutation_method=mut,
        stopping_condition=stop,
        use_elite=elite,
        track_convergence=diffs
    )
    return best_individual, sum(best_individual), abs(sum(best_individual) - target), diffs


# Funkcja do rysowania wykresu konwergencji dla 5 przebiegów
def plot_multiple_convergence_curves(results):
    algos = list(results.keys())
    plt.figure(figsize=(12, 8))

    for algo in algos:
        for i, convergence in enumerate(results[algo]["convergences"]):
            if convergence:
                plt.plot(range(len(convergence)), convergence, label=f"{algo} - Run {i+1}")

    plt.xlabel('Iteracje')
    plt.ylabel('Różnica do Celu')
    plt.title('Krzywa Zbieżności (5 przebiegów dla każdego algorytmu)')
    plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1))
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("convergence_curve_multiple_runs.png")
    plt.show()


# Funkcja do obliczania średniej krzywej zbieżności
def calculate_average_convergence(convergences):
    max_length = max(len(convergence) for convergence in convergences)
    average_convergence = np.zeros(max_length)

    for convergence in convergences:
        for i in range(len(convergence)):
            average_convergence[i] += convergence[i]

    average_convergence /= len(convergences)
    return average_convergence


# Funkcja do rysowania wykresu średniej krzywej zbieżności (osobny wykres)
def plot_average_convergence(results):
    algos = list(results.keys())
    plt.figure(figsize=(12, 8))

    for algo in algos:
        # Oblicz średnią zbieżność dla każdego algorytmu
        average_convergence = calculate_average_convergence(results[algo]["convergences"])

        # Rysuj średnią krzywą zbieżności
        plt.plot(range(len(average_convergence)), average_convergence, label=f"{algo} - Average", linestyle='-',
                 linewidth=2)

    plt.xlabel('Iteracje')
    plt.ylabel('Różnica do Celu')
    plt.title('Średnia Krzywa Zbieżności dla Algorytmów')
    plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1))
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("average_convergence_curve.png")  # Zapisz wykres
    plt.show()


# Funkcja do rysowania wyników: Czas wykonania, Zużycie pamięci, Różnica do celu
def plot_results(results):
    algos = list(results.keys())
    exec_times = [results[a]["execution_time"] for a in algos]
    mem_usages = [results[a]["memory_usage"] for a in algos]
    differences = [results[a]["difference"] for a in algos]

    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height,
                     f'{height:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Wykres czasu wykonania
    plt.figure(figsize=(10, 6))
    bars = plt.bar(algos, exec_times, color='skyblue')
    add_labels(bars)
    plt.ylabel('Czas wykonania (s)')
    plt.title('Porównanie czasu wykonania algorytmów')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("execution_time.png")
    plt.show()

    # Wykres użycia pamięci
    plt.figure(figsize=(10, 6))
    bars = plt.bar(algos, mem_usages, color='salmon')
    add_labels(bars)
    plt.ylabel('Zużycie pamięci (MB)')
    plt.title('Porównanie zużycia pamięci przez algorytmy')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("memory_usage.png")
    plt.show()

    # Wykres różnicy do celu
    plt.figure(figsize=(10, 6))
    bars = plt.bar(algos, differences, color='lightgreen')
    add_labels(bars)
    plt.ylabel('Różnica do celu')
    plt.title('Porównanie dokładności algorytmów')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("difference_to_target.png")
    plt.show()

    # Wykres średniej krzywej zbieżności
    plot_average_convergence(results)


class DummyFile(object):
    def write(self, x): pass


# Funkcja zbierająca wszystkie algorytmy
def run_comparison(file, target,suppress=True):
    if suppress == True:
        sys.stdout = DummyFile()
    algorithms = {
        "bruteforce": lambda: run_bruteforce(file, target),
        "hillclimb_best": lambda: run_hillclimb(file, target, mode="best"),
        "hillclimb_random": lambda: run_hillclimb(file, target, mode="random"),
        "genetic": lambda: run_genetic(file, target, pop=50, cross="one_point", mut="add_remove", stop="no_improve",
                                       elite=1),
        "geneticNew": lambda: run_genetic_new(file, target, pop=50, cross="uniform", mrate=0.1, stop="generations",
                                              elite=1, generations=100),
        "simulated": lambda: run_simulated(file, target, schedule="exponential", alpha=0.9),
        "tabu": lambda: run_tabu(file, target, tabu_size=10)
    }

    results = {}
    for algo_name, algo_func in algorithms.items():
        print(f"Running {algo_name}...")

        exec_times = []
        mem_usages = []
        differences = []
        all_convergences = []

        for i in range(5):  # 5-krotny test
            result, exec_time, mem_usage = measure_performance(algo_func)

            if isinstance(result, tuple):
                if len(result) == 3:
                    difference = result[2]
                    convergence = []
                elif len(result) == 4:
                    _, _, difference, convergence = result
                else:
                    print(f"Błąd: algorytm zwrócił więcej niż 4 wartości: {result}")
                    continue
            else:
                difference = 0
                convergence = []

            exec_times.append(exec_time)
            mem_usages.append(mem_usage)
            differences.append(difference)
            all_convergences.append(convergence)

        results[algo_name] = {
            "execution_time": sum(exec_times) / len(exec_times),
            "memory_usage": sum(mem_usages) / len(mem_usages),
            "difference": sum(differences) / len(differences),
            "convergences": all_convergences
        }
    if suppress:
        sys.stdout = sys.stdout
    plot_results(results)
    plot_multiple_convergence_curves(results)  # Generowanie wykresu dla 5 przebiegów

    print(f"{'Algorytm':<20}{'Czas Wykonania (s)':<20}{'Użycie Pamięci (MB)':<20}{'Różnica do Celu':<20}")
    for algo_name, result in results.items():
        print(
            f"{algo_name:<20}{result['execution_time']:<20.4f}{result['memory_usage']:<20.4f}{result['difference']:<20}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Algorytmy optymalizacji dla Subset Sum Problem ( SSP ).")
    parser.add_argument("--file", required=True, help="Plik wejściowy")
    parser.add_argument("--target", type=int, required=True, help="Suma jaka chcesz osiagnac")
    parser.add_argument("--suppress", type=int, choices=[0, 1], default=0)
    args = parser.parse_args()



    run_comparison(args.file, args.target)
