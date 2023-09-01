from constants import *
from delivery_request import DeliveryRequest
from genetic_algorithm import *
from point import Point


class Model:
    DEFAULT_DELIVERY_COUNT = 8
    DEFAULT_DRONE_COUNT = 3

    delivery_requests = []
    targets = []
    paths = []
    distance_matrix = np.empty((0, 0))
    station = Point(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)

    best_distance = None
    best_time = None

    def generate_targets(self, count=DEFAULT_DELIVERY_COUNT):
        self.delivery_requests = [DeliveryRequest.random() for _ in range(count)]
        self.targets = self.delivery_requests[:]
        # Station is added as DeliveryRequest with start and end at the same point
        self.targets.insert(0, DeliveryRequest(self.station.x, self.station.y, self.station.x, self.station.y))
        self.calculate_distance_matrix()

    def calculate_distance_matrix(self):
        self.distance_matrix = np.zeros((len(self.targets), len(self.targets)))
        for i, delivery1 in enumerate(self.targets):
            for j, delivery2 in enumerate(self.targets):
                self.distance_matrix[i, j] = delivery1.end.distance(delivery2.start) + delivery2.distance

    def generate_paths(self, count=DEFAULT_DRONE_COUNT, size=60, generations=100):
        pop1, pop2 = generate_population(len(self.delivery_requests), count, size)
        result, solutions = evaluate(pop1, pop2, self.calculate_total_distance)
        scores = result[:, 0]
        min_index = np.argmin(scores)

        best_solution = solutions[min_index]
        best_score = result[min_index][0]
        self.best_distance = result[min_index][1]
        self.best_time = result[min_index][2]

        for _ in range(generations):
            pop1, pop2 = selection(pop1, pop2, scores)
            pop1 = crossover(pop1, 0.7)
            pop1 = mutation(pop1, swap_mutation_logic, 0.1)
            pop2 = mutation(pop2, add_subtract_mutation_logic, 0.1)

            result, solutions = evaluate(pop1, pop2, self.calculate_total_distance)
            scores = result[:, 0]
            min_index = np.argmin(scores)
            temp_best_score = result[min_index][0]

            if best_score > temp_best_score:
                best_score = temp_best_score
                best_solution = solutions[min_index]
                self.best_distance = result[min_index][1]
                self.best_time = result[min_index][2]

        print(best_solution)
        print(self.best_time)
        print(self.best_distance)

        self.calculate_paths_vectors(best_solution)

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
