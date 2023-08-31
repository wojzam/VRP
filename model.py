import numpy as np

from constants import *
from delivery_request import DeliveryRequest
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

    def generate_paths(self, count=DEFAULT_DRONE_COUNT, generations=1000):
        best_score = float('inf')
        self.best_distance = None
        self.best_time = None
        best_solution = None

        pop1, pop2 = Model.generate_population(len(self.delivery_requests), count, generations)

        for row1, row2 in zip(pop1, pop2):
            solution = self.decode_solution(row1, row2)
            distances = [self.calculate_total_distance(np.array(drone)) for drone in solution]
            total_distance = sum(distances)
            time = max(distances)
            score = total_distance + 2 * time

            if best_score > score:
                best_score = score
                self.best_distance = total_distance
                self.best_time = time
                best_solution = solution

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

    @staticmethod
    def generate_population(requests_count, drones_count, size):
        pop1 = np.array([np.random.permutation(requests_count) + 1 for _ in range(size)])
        pop2 = np.array([Model.create_array_with_sum(requests_count, drones_count) for _ in range(size)])
        return pop1, pop2

    @staticmethod
    def decode_solution(row1, row2):
        solution = []
        index = 0
        for count in row2:
            paths = [0] + [row1[index + i] for i in range(count)]
            solution.append(paths)
            index += count
        return solution

    @staticmethod
    def create_array_with_sum(total_sum, size):
        return np.bincount(np.random.randint(size, size=total_sum), minlength=size)
