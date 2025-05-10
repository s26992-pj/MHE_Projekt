def generate_neighbors(solution, all_numbers):
    neighbors = set()

    # Zamień jeden element na inny (modyfikacja)
    for i in range(len(solution)):
        for n in all_numbers:
            if n not in solution:
                new_solution = solution[:i] + [n] + solution[i+1:]
                neighbors.add(tuple(sorted(new_solution)))

    # Dodaj jeden nowy element
    for n in all_numbers:
        if n not in solution:
            new_solution = solution + [n]
            neighbors.add(tuple(sorted(new_solution)))

    # Usuń jeden element
    if len(solution) > 1:
        for i in range(len(solution)):
            new_solution = solution[:i] + solution[i+1:]
            neighbors.add(tuple(sorted(new_solution)))

    # Konwersja z powrotem do list
    return [list(n) for n in neighbors]