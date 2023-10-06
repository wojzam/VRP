import numpy as np


def order_crossover(parent1, parent2):
    size = len(parent1)
    cx1, cx2 = np.sort(np.random.choice(size + 1, 2, replace=False))

    missing1 = parent2[~np.isin(parent2, parent1[cx1:cx2])]
    missing2 = parent1[~np.isin(parent1, parent2[cx1:cx2])]

    offspring1 = np.empty(size, dtype=int)
    offspring2 = np.empty(size, dtype=int)

    offspring1[:cx1] = missing1[:cx1]
    offspring2[:cx1] = missing2[:cx1]
    offspring1[cx1:cx2] = parent1[cx1:cx2]
    offspring2[cx1:cx2] = parent2[cx1:cx2]
    offspring1[cx2:] = missing1[cx1:]
    offspring2[cx2:] = missing2[cx1:]

    return offspring1, offspring2


def shuffle_mutation(individual):
    size = len(individual)
    subset_size = np.random.randint(min(2, size), size + 1)
    indices = np.random.choice(size, size=subset_size, replace=False)
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
