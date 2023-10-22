import numpy as np


def order_crossover(parent1, parent2):
    size = len(parent1)
    cx1, cx2 = np.sort(np.random.choice(size + 1, 2, replace=False))

    missing1 = parent2[~np.isin(parent2, parent1[cx1:cx2])]
    missing2 = parent1[~np.isin(parent1, parent2[cx1:cx2])]

    offspring1, offspring2 = np.empty(size, dtype=int), np.empty(size, dtype=int)

    offspring1[:cx1] = missing1[:cx1]
    offspring2[:cx1] = missing2[:cx1]
    offspring1[cx1:cx2] = parent1[cx1:cx2]
    offspring2[cx1:cx2] = parent2[cx1:cx2]
    offspring1[cx2:] = missing1[cx1:]
    offspring2[cx2:] = missing2[cx1:]

    return offspring1, offspring2


def order_based_crossover(parent1, parent2):
    size = len(parent1)
    selected = np.random.choice([True, False], size)

    matching1 = np.isin(parent2, parent1[selected])
    matching2 = np.isin(parent1, parent2[selected])

    offspring1, offspring2 = np.empty(size, dtype=int), np.empty(size, dtype=int)

    offspring1[matching1] = parent1[selected]
    offspring2[matching2] = parent2[selected]
    offspring1[~matching1] = parent2[~matching1]
    offspring2[~matching2] = parent1[~matching2]

    return offspring1, offspring2


def position_based_crossover(parent1, parent2):
    size = len(parent1)
    selected = np.random.choice([True, False], size)

    offspring1, offspring2 = np.empty(size, dtype=int), np.empty(size, dtype=int)

    offspring1[selected] = parent1[selected]
    offspring2[selected] = parent2[selected]
    offspring1[~selected] = parent2[~np.isin(parent2, parent1[selected])]
    offspring2[~selected] = parent1[~np.isin(parent1, parent2[selected])]

    return offspring1, offspring2


def cycle_crossover(parent1, parent2):
    size = len(parent1)
    offspring1, offspring2 = np.empty(size, dtype=int), np.empty(size, dtype=int)
    visited = np.zeros(size, dtype=bool)
    source1, source2 = parent1, parent2

    for start in range(size):
        if visited[start]:
            continue
        visited[start] = True
        cycle = [start]

        while parent2[cycle[-1]] != parent1[start]:
            next_index = np.where(parent1 == parent2[cycle[-1]])[0][0]
            cycle.append(next_index)
            visited[next_index] = True

        cycle = np.array(cycle)
        offspring1[cycle] = source1[cycle]
        offspring2[cycle] = source2[cycle]

        source1, source2 = source2, source1

    return offspring1, offspring2


def partially_mapped_crossover(parent1, parent2):
    size = len(parent1)
    cx1, cx2 = np.sort(np.random.choice(size + 1, 2, replace=False))

    def one_offspring(p1, p2):
        offspring = np.empty(size, dtype=int)
        offspring[cx1:cx2] = p1[cx1:cx2]

        for i in np.concatenate([np.arange(0, cx1), np.arange(cx2, size)]):
            candidate = p2[i]
            while candidate in p1[cx1:cx2]:
                candidate = p2[np.where(p1 == candidate)[0][0]]
            offspring[i] = candidate
        return offspring

    return one_offspring(parent1, parent2), one_offspring(parent2, parent1)


def shuffle_mutation(individual):
    size = len(individual)
    indices = np.random.choice([True, False], size)
    subset = individual[indices]
    np.random.shuffle(subset)
    individual[indices] = subset


def add_subtract_mutation(individual):
    idx1 = np.random.choice(np.nonzero(individual)[0])
    idx2 = idx1
    while idx2 == idx1:
        idx2 = np.random.randint(len(individual))

    individual[idx1] -= 1
    individual[idx2] += 1
