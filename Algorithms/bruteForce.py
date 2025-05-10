import itertools


def brute_force(numbers, target,track_convergence=None):
    bestSubset = []
    #ustawiona na nieskończoność przechowuje najmniejszą różnice między sumą a docelową
    best_diff = float('inf')

    if track_convergence is None:
        track_convergence = []

    for r in range(1, len(numbers) + 1):
        for subset in itertools.combinations(numbers, r):
            total = sum(subset)
            diff = abs(total - target)

            track_convergence.append(diff)

            if diff < best_diff:
                bestSubset = subset
                best_diff = diff
                if diff == 0:
                    return list(bestSubset), total, diff, track_convergence

    return list(bestSubset), sum(bestSubset), abs(sum(bestSubset) - target), track_convergence
