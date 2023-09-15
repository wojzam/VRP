import numpy as np
import matplotlib.pyplot as plt


def generate_population(requests_count, drones_count, size):
    pop1 = np.array([np.random.permutation(requests_count) + 1 for _ in range(size)])
    pop2 = np.array([create_array_with_sum(requests_count, drones_count) for _ in range(size)])
    return pop1, pop2


def generate_population_2(requests_count, drones_count, size):
    return np.array([np.random.permutation(requests_count + drones_count - 1) + 1 for _ in range(size)])


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


def decode_individual_2(row, drones_count):
    solution = []
    delivery_threshold = len(row) - drones_count + 1
    paths = [0]
    for value in row:
        if value > delivery_threshold:
            solution.append(paths)
            paths = [0]
        else:
            paths.append(value)
    solution.append(paths)

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


def evaluate_2(pop, drones_count, calculate_total_distance):
    evaluated_pop = []
    decoded = []
    for row in pop:
        solution = decode_individual_2(row, drones_count)
        distances = [calculate_total_distance(np.array(drone)) for drone in solution]

        total_distance = sum(distances)
        time = max(distances)
        score = total_distance + 2 * time

        evaluated_pop.append([score, total_distance, time])
        decoded.append(solution)

    return np.array(evaluated_pop), decoded


def selection(*args, scores):
    inverted_scores = 1 / scores
    probabilities = inverted_scores / np.sum(inverted_scores)
    selected_indices = np.random.choice(len(args[0]), p=probabilities, size=len(args[0]))

    if len(args) == 1:
        return args[0][selected_indices]

    return (pop[selected_indices] for pop in args)


def crossover(population, p=1.):
    new_pop = np.copy(population)
    num_individuals, num_genes = population.shape
    for i in range(0, num_individuals - 1, 2):
        if np.random.uniform() < p:
            new_pop[i], new_pop[i + 1] = order_crossover(new_pop[i], new_pop[i + 1])
    return new_pop


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


def mutation(population, mutation_logic, p=1.):
    new_pop = population.copy()
    num_individuals, num_genes = population.shape
    if num_genes > 1:
        for i in range(num_individuals):
            if np.random.uniform() < p:
                mutation_logic(new_pop[i])
    return new_pop


def shuffle_mutation_logic(individual):
    size = len(individual)
    subset_size = np.random.randint(min(2, size), size + 1)
    indices = np.random.choice(size, size=subset_size, replace=False)
    subset = individual[indices]
    np.random.shuffle(subset)
    individual[indices] = subset


def add_subtract_mutation_logic(individual):
    idx1 = np.random.choice(np.nonzero(individual)[0])
    idx2 = idx1
    while idx2 == idx1:
        idx2 = np.random.randint(len(individual))

    individual[idx1] -= 1
    individual[idx2] += 1


def evolve(requests_count, drones_count, size, generations, evaluation_function, show_plot=True):
    pop1, pop2 = generate_population(requests_count, drones_count, size)
    result, solutions = evaluate(pop1, pop2, evaluation_function)
    scores = result[:, 0]
    min_index = np.argmin(scores)

    best_solution = solutions[min_index]
    best_score = result[min_index][0]
    best_distance = result[min_index][1]
    best_time = result[min_index][2]
    global_best_scores = []
    best_scores = []
    mean_scores = []

    for _ in range(generations):
        pop1, pop2 = selection(pop1, pop2, scores=scores)
        pop1 = crossover(pop1, 0.7)
        pop1 = mutation(pop1, shuffle_mutation_logic, 0.1)
        pop2 = mutation(pop2, add_subtract_mutation_logic, 0.05)

        result, solutions = evaluate(pop1, pop2, evaluation_function)
        scores = result[:, 0]
        min_index = np.argmin(scores)
        temp_best_score = result[min_index][0]

        if best_score > temp_best_score:
            best_score = temp_best_score
            best_solution = solutions[min_index]
            best_distance = result[min_index][1]
            best_time = result[min_index][2]

        global_best_scores.append(best_score)
        best_scores.append(temp_best_score)
        mean_scores.append(np.average(scores))

    if show_plot:
        plot(global_best_scores, best_scores, mean_scores)

    return best_solution, best_distance, best_time


def evolve_2(requests_count, drones_count, size, generations, evaluation_function, show_plot=True):
    pop = generate_population_2(requests_count, drones_count, size)
    result, solutions = evaluate_2(pop, drones_count, evaluation_function)
    scores = result[:, 0]
    min_index = np.argmin(scores)

    best_solution = solutions[min_index]
    best_score = result[min_index][0]
    best_distance = result[min_index][1]
    best_time = result[min_index][2]
    global_best_scores = []
    best_scores = []
    mean_scores = []

    for _ in range(generations):
        pop = selection(pop, scores=scores)
        pop = crossover(pop, 0.7)
        pop = mutation(pop, shuffle_mutation_logic, 0.1)

        result, solutions = evaluate_2(pop, drones_count, evaluation_function)
        scores = result[:, 0]
        min_index = np.argmin(scores)
        temp_best_score = result[min_index][0]

        if best_score > temp_best_score:
            best_score = temp_best_score
            best_solution = solutions[min_index]
            best_distance = result[min_index][1]
            best_time = result[min_index][2]

        global_best_scores.append(best_score)
        best_scores.append(temp_best_score)
        mean_scores.append(np.average(scores))

    if show_plot:
        plot(global_best_scores, best_scores, mean_scores)

    return best_solution, best_distance, best_time


def plot(global_best_scores, best_scores, mean_scores):
    plt.figure(figsize=(10, 5))
    plt.plot(range(len(global_best_scores)), global_best_scores, label='Global Best Score', marker='o')
    plt.plot(range(len(best_scores)), best_scores, label='Best Score', marker='x')
    plt.plot(range(len(mean_scores)), mean_scores, label='Mean Score', marker='x')
    plt.xlabel('Generation')
    plt.ylabel('Score')
    plt.legend()
    plt.title('Evolution of Best Scores')
    plt.grid(True)
    plt.show()
