import numpy as np

from constants import *
from delivery_request import DeliveryRequest
from genetic_algorithm import GeneticAlgorithm
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
        ga = GeneticAlgorithm(len(self.delivery_requests), count, self.calculate_total_distance)
        best_solution, self.best_distance, self.best_time = ga.evolve(size, generations)

        self.calculate_paths_vectors(best_solution)

        print(best_solution)
        print(self.best_time)
        print(self.best_distance)

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
