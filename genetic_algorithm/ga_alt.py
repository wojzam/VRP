from genetic_algorithm.ga import *


# TODO: Reduce code duplication
class GAAlt(GA):

    def generate_population(self, size):
        pop1 = np.array([np.random.permutation(self.requests_count) + 1 for _ in range(size)])
        pop2 = np.array([self.create_array_with_sum(self.requests_count, self.vehicles_count) for _ in range(size)])

        return pop1, pop2

    @staticmethod
    def create_array_with_sum(total_sum, size):
        return np.bincount(np.random.randint(size, size=total_sum), minlength=size)

    def evaluate(self, pop):
        evaluated_pop = []
        decoded = []
        for row in zip(*pop):
            solution = self.decode_individual(row)
            distances = [self.calculate_distance(np.array(vehicle)) for vehicle in solution]

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
            routes = [0] + [row[0][index + i] for i in range(count)]
            solution.append(routes)
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
                new_pop[i], new_pop[i + 1] = order_crossover(new_pop[i], new_pop[i + 1])

        return new_pop, population[1]

    def mutation(self, population, p=1.):
        new_pop1 = population[0].copy()
        new_pop2 = population[1].copy()
        num_individuals, num_genes = new_pop1.shape
        if num_genes > 1:
            for i in range(num_individuals):
                if np.random.uniform() < p:
                    shuffle_mutation(new_pop1[i])
                if np.random.uniform() < p:
                    add_subtract_mutation(new_pop2[i])
        return new_pop1, new_pop2
