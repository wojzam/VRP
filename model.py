import matplotlib.pyplot as plt

from constants import *
from delivery_request import DeliveryRequest
from genetic_algorithm import *
from point import Point


class Model:
    DEFAULT_DELIVERIES_COUNT = 6
    DEFAULT_DRONES_COUNT = 3
    DEFAULT_GENERATIONS = 100
    DEFAULT_POP_SIZE = 60

    delivery_requests = []
    targets = []
    paths = []
    distance_matrix = np.empty((0, 0))
    station = Point(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)

    best_distance = 0
    best_time = 0

    def clear_solution(self):
        self.best_distance = 0
        self.best_time = 0
        self.paths = []

    def generate_targets(self, count=DEFAULT_DELIVERIES_COUNT):
        self.delivery_requests = [DeliveryRequest.random() for _ in range(count)]
        self.targets = self.delivery_requests[:]
        # Station is added as DeliveryRequest with start and end at the same point
        self.targets.insert(0, DeliveryRequest(self.station.x, self.station.y, self.station.x, self.station.y))
        self.calculate_distance_matrix()
        self.clear_solution()

    def calculate_distance_matrix(self):
        self.distance_matrix = np.zeros((len(self.targets), len(self.targets)))
        for i, delivery1 in enumerate(self.targets):
            for j, delivery2 in enumerate(self.targets):
                self.distance_matrix[i, j] = delivery1.end.distance(delivery2.start) + delivery2.distance

    def generate_paths(self, count=DEFAULT_DRONES_COUNT, size=DEFAULT_POP_SIZE, generations=DEFAULT_GENERATIONS):
        pop1, pop2 = generate_population(len(self.delivery_requests), count, size)
        result, solutions = evaluate(pop1, pop2, self.calculate_total_distance)
        scores = result[:, 0]
        min_index = np.argmin(scores)

        best_solution = solutions[min_index]
        best_score = result[min_index][0]
        self.best_distance = result[min_index][1]
        self.best_time = result[min_index][2]
        global_best_scores = []
        best_scores = []
        mean_scores = []

        for _ in range(generations):
            pop1, pop2 = selection(pop1, pop2, scores)
            pop1 = crossover(pop1, 0.7)
            pop1 = mutation(pop1, shuffle_mutation_logic, 0.1)
            pop2 = mutation(pop2, add_subtract_mutation_logic, 0.05)

            result, solutions = evaluate(pop1, pop2, self.calculate_total_distance)
            scores = result[:, 0]
            min_index = np.argmin(scores)
            temp_best_score = result[min_index][0]

            if best_score > temp_best_score:
                best_score = temp_best_score
                best_solution = solutions[min_index]
                self.best_distance = result[min_index][1]
                self.best_time = result[min_index][2]

            global_best_scores.append(best_score)
            best_scores.append(temp_best_score)
            mean_scores.append(np.average(scores))

        print(best_solution)
        print(self.best_time)
        print(self.best_distance)

        self.calculate_paths_vectors(best_solution)
        self.show_plot(global_best_scores, best_scores, mean_scores)

    def calculate_paths_vectors(self, solution):
        self.paths = []
        for path in solution:
            vectors = []
            for i in range(1, len(path)):
                current = self.targets[path[i]]
                previous = self.targets[path[i - 1]]
                vectors.append((current.start, current.end))
                vectors.append((previous.end, current.start))

            self.paths.append(vectors)

    def calculate_total_distance(self, paths):
        return np.sum(self.distance_matrix[paths[:-1], paths[1:]])

    @staticmethod
    def show_plot(global_best_scores, best_scores, mean_scores):
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
