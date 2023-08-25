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

    def generate_paths(self, count=DEFAULT_DRONE_COUNT, generations=10000):
        best_score = None
        best_distance = None
        best_time = None
        best_solution = None

        for _ in range(generations):
            solution = self.random_solution(count)
            distances = [self.calculate_total_distance(np.array(drone)) for drone in solution]
            total_distance = sum(distances)
            time = max(distances)
            score = total_distance + 2 * time

            if best_score is None or best_score > score:
                best_score = score
                best_distance = total_distance
                best_time = time
                best_solution = solution

        print(best_solution)
        print(best_time)
        print(best_distance)

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

    def random_solution(self, count=DEFAULT_DRONE_COUNT):
        targets_indexes = np.arange(1, len(self.targets))
        np.random.shuffle(targets_indexes)
        random_drones = np.random.randint(count, size=(len(targets_indexes)))
        solution = [[0] for _ in range(count)]

        for drone, delivery_idx in zip(random_drones, targets_indexes):
            solution[drone].append(delivery_idx)

        return solution

    def calculate_total_distance(self, paths):
        return np.sum(self.distance_matrix[paths[:-1], paths[1:]])
