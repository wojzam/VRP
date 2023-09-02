import numpy as np


def generate_population(requests_count, drones_count, size):
    pop1 = np.array([np.random.permutation(requests_count) + 1 for _ in range(size)])
    pop2 = np.array([create_array_with_sum(requests_count, drones_count) for _ in range(size)])
    return pop1, pop2


def create_array_with_sum(total_sum, size):
    return np.bincount(np.random.randint(size, size=total_sum), minlength=size)


def decode_individual(row1, row2):
    solution = []
    index = 0
    for count in row2:
        paths = [0] + [row1[index + i] for i in range(count)]
        solution.append(paths)
        index += count
    return solution


def evaluate(pop1, pop2, calculate_total_distance):
    evaluated_pop = []
    decoded = []
    for row1, row2 in zip(pop1, pop2):
        solution = decode_individual(row1, row2)
        distances = [calculate_total_distance(np.array(drone)) for drone in solution]

        total_distance = sum(distances)
        time = max(distances)
        score = total_distance + 2 * time

        evaluated_pop.append([score, total_distance, time])
        decoded.append(solution)

    return np.array(evaluated_pop), decoded


def selection(pop1, pop2, scores):
    inverted_scores = 1 / scores
    probabilities = inverted_scores / np.sum(inverted_scores)
    selected_indices = np.random.choice(len(pop1), p=probabilities, size=len(pop1))
    return pop1[selected_indices], pop2[selected_indices]


def crossover(population, p=1):
    new_pop = np.copy(population)
    num_individuals, num_genes = population.shape
    for i in range(0, num_individuals - 1, 2):
        if np.random.uniform() < p:
            new_pop[i], new_pop[i + 1] = partially_mapped_crossover(new_pop[i], new_pop[i + 1])
    return new_pop


def partially_mapped_crossover(parent1, parent2):
    size = len(parent1)
    offspring1 = np.zeros(size, dtype=int)
    offspring2 = np.zeros(size, dtype=int)

    cx1, cx2 = np.sort(np.random.choice(size - 1, 2, replace=False) + 1)

    offspring1[cx1:cx2] = parent1[cx1:cx2]
    offspring2[cx1:cx2] = parent2[cx1:cx2]

    missing1 = parent2[~np.isin(parent2, offspring1[cx1:cx2])]
    missing2 = parent1[~np.isin(parent1, offspring2[cx1:cx2])]

    idx = 0
    while cx2 != cx1:
        offspring1[cx2] = missing1[idx]
        offspring2[cx2] = missing2[idx]
        cx2 = (cx2 + 1) % size
        idx += 1

    return offspring1, offspring2


def mutation(population, mutation_logic, p=1):
    new_pop = population.copy()
    num_individuals, num_genes = population.shape
    if num_genes > 1:
        for i in range(num_individuals):
            if np.random.uniform() < p:
                mutation_logic(new_pop[i])
    return new_pop


def swap_mutation_logic(individual):
    idx1, idx2 = np.random.choice(len(individual), size=2, replace=False)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]


def add_subtract_mutation_logic(individual):
    idx1 = np.random.choice(np.nonzero(individual)[0])
    idx2 = idx1
    while idx2 == idx1:
        idx2 = np.random.randint(len(individual))

    individual[idx1] -= 1
    individual[idx2] += 1
