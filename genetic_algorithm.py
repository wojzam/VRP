import matplotlib.pyplot as plt
import numpy as np


class GeneticAlgorithm:

    def __init__(self, requests_count, drones_count, calculate_distance):
        self.requests_count = requests_count
        self.drones_count = drones_count
        self.calculate_distance = calculate_distance

    def evolve(self, size, generations, show_plot=True):
        pop = self.generate_population(size)
        result, solutions = self.evaluate(pop)
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
            pop = self.selection(pop, scores=scores)
            pop = self.crossover(pop, 0.7)
            pop = self.mutation(pop, 0.1)

            result, solutions = self.evaluate(pop)
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
            self.plot(global_best_scores, best_scores, mean_scores)

        return best_solution, best_distance, best_time

    def generate_population(self, size):
        return np.array([np.random.permutation(self.requests_count + self.drones_count - 1) + 1 for _ in range(size)])

    def decode_individual(self, row):
        solution = []
        delivery_threshold = len(row) - self.drones_count + 1
        paths = [0]
        for value in row:
            if value > delivery_threshold:
                solution.append(paths)
                paths = [0]
            else:
                paths.append(value)
        solution.append(paths)

        return solution

    def evaluate(self, pop):
        evaluated_pop = []
        decoded = []
        for row in pop:
            solution = self.decode_individual(row)
            distances = [self.calculate_distance(np.array(drone)) for drone in solution]

            total_distance = sum(distances)
            time = max(distances)
            score = total_distance + 2 * time

            evaluated_pop.append([score, total_distance, time])
            decoded.append(solution)

        return np.array(evaluated_pop), decoded

    @staticmethod
    def selection(population, scores):
        inverted_scores = 1 / scores
        probabilities = inverted_scores / np.sum(inverted_scores)
        selected_indices = np.random.choice(len(population), p=probabilities, size=len(population))

        return population[selected_indices]

    def crossover(self, population, p=1.):
        new_pop = np.copy(population)
        num_individuals, num_genes = new_pop.shape
        for i in range(0, num_individuals - 1, 2):
            if np.random.uniform() < p:
                new_pop[i], new_pop[i + 1] = self.order_crossover(new_pop[i], new_pop[i + 1])

        return new_pop

    @staticmethod
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

    def mutation(self, population, p=1.):
        new_pop = population.copy()
        num_individuals, num_genes = new_pop.shape
        if num_genes > 1:
            for i in range(num_individuals):
                if np.random.uniform() < p:
                    self.shuffle_mutation_logic(new_pop[i])
        return new_pop

    @staticmethod
    def shuffle_mutation_logic(individual):
        size = len(individual)
        subset_size = np.random.randint(min(2, size), size + 1)
        indices = np.random.choice(size, size=subset_size, replace=False)
        subset = individual[indices]
        np.random.shuffle(subset)
        individual[indices] = subset

    @staticmethod
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


# TODO: Reduce code duplication
class GeneticAlgorithm2(GeneticAlgorithm):

    def generate_population(self, size):
        pop1 = np.array([np.random.permutation(self.requests_count) + 1 for _ in range(size)])
        pop2 = np.array([self.create_array_with_sum(self.requests_count, self.drones_count) for _ in range(size)])

        return pop1, pop2

    @staticmethod
    def create_array_with_sum(total_sum, size):
        return np.bincount(np.random.randint(size, size=total_sum), minlength=size)

    def evaluate(self, pop):
        evaluated_pop = []
        decoded = []
        for row in zip(*pop):
            solution = self.decode_individual(row)
            distances = [self.calculate_distance(np.array(drone)) for drone in solution]

            total_distance = sum(distances)
            time = max(distances)
            score = total_distance + 2 * time

            evaluated_pop.append([score, total_distance, time])
            decoded.append(solution)

        return np.array(evaluated_pop), decoded

    def decode_individual(self, row):
        solution = []
        index = 0
        for count in row[1]:
            paths = [0] + [row[0][index + i] for i in range(count)]
            solution.append(paths)
            index += count
        return solution

    @staticmethod
    def selection(population, scores):
        inverted_scores = 1 / scores
        probabilities = inverted_scores / np.sum(inverted_scores)
        selected_indices = np.random.choice(len(population[0]), p=probabilities, size=len(population[0]))

        return tuple(pop[selected_indices] for pop in population)

    def crossover(self, population, p=1.):
        new_pop = np.copy(population[0])
        num_individuals, num_genes = new_pop.shape
        for i in range(0, num_individuals - 1, 2):
            if np.random.uniform() < p:
                new_pop[i], new_pop[i + 1] = self.order_crossover(new_pop[i], new_pop[i + 1])

        return new_pop, population[1]

    def mutation(self, population, p=1.):
        new_pop1 = population[0].copy()
        new_pop2 = population[1].copy()
        num_individuals, num_genes = new_pop1.shape
        if num_genes > 1:
            for i in range(num_individuals):
                if np.random.uniform() < p:
                    self.shuffle_mutation_logic(new_pop1[i])
                if np.random.uniform() < p:
                    self.add_subtract_mutation_logic(new_pop2[i])
        return new_pop1, new_pop2

    @staticmethod
    def add_subtract_mutation_logic(individual):
        idx1 = np.random.choice(np.nonzero(individual)[0])
        idx2 = idx1
        while idx2 == idx1:
            idx2 = np.random.randint(len(individual))

        individual[idx1] -= 1
        individual[idx2] += 1
