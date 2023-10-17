from genetic_algorithm.strategies import *
from genetic_algorithm.utils import *


class GA:

    def __init__(self, customers_count, vehicles_count, distance_factor, time_factor, calculate_distance_func):
        self.customers_count = customers_count
        self.vehicles_count = vehicles_count
        self.distance_factor = distance_factor
        self.time_factor = time_factor
        self.calculate_distance_func = calculate_distance_func

    def evolve(self, size, generations, pc, pm, show_plot=True):
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
            pop = self.crossover(pop, pc)
            pop = self.mutation(pop, pm)

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
            plot_results(global_best_scores, best_scores, mean_scores)

        return best_solution, best_distance, best_time, best_score

    def generate_population(self, size):
        return np.array(
            [np.random.permutation(self.customers_count + self.vehicles_count - 1) + 1 for _ in range(size)])

    def decode_individual(self, row):
        solution = []
        highest_customer_index = len(row) - self.vehicles_count + 1
        routes = [0]
        for value in row:
            if value > highest_customer_index:
                solution.append(routes)
                routes = [0]
            else:
                routes.append(value)
        solution.append(routes)

        return solution

    def evaluate(self, pop):
        evaluated_pop = []
        decoded = []
        for row in pop:
            solution = self.decode_individual(row)
            distances = [self.calculate_distance_func(np.array(vehicle)) for vehicle in solution]

            total_distance = sum(distances)
            time = max(distances)
            score = self.calculate_score(total_distance, time)

            evaluated_pop.append([score, total_distance, time])
            decoded.append(solution)

        return np.array(evaluated_pop), decoded

    def calculate_score(self, total_distance, time):
        return self.distance_factor * total_distance + self.time_factor * time

    @staticmethod
    def selection(population, scores):
        inverted_scores = 1 / scores
        probabilities = inverted_scores / np.sum(inverted_scores)
        selected_indices = np.random.choice(len(population), p=probabilities, size=len(population))

        return population[selected_indices]

    @staticmethod
    def crossover(population, p=1.):
        new_pop = np.copy(population)
        num_individuals, num_genes = new_pop.shape
        for i in range(0, num_individuals - 1, 2):
            if np.random.uniform() < p:
                new_pop[i], new_pop[i + 1] = order_crossover(new_pop[i], new_pop[i + 1])

        return new_pop

    @staticmethod
    def mutation(population, p=1.):
        new_pop = population.copy()
        num_individuals, num_genes = new_pop.shape
        if num_genes > 1:
            for i in range(num_individuals):
                if np.random.uniform() < p:
                    shuffle_mutation(new_pop[i])
        return new_pop
