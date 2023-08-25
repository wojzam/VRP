import numpy as np

from constants import *
from delivery_request import DeliveryRequest
from point import Point


class Model:
    DEFAULT_DELIVERY_COUNT = 5
    DEFAULT_DRONE_COUNT = 3

    delivery_requests = []
    drones_tasks = []
    distance_matrix = np.empty((0, 0))
    station = Point(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)

    def generate_delivery_requests(self, count=DEFAULT_DELIVERY_COUNT):
        self.delivery_requests = [DeliveryRequest.random() for _ in range(count)]
        self.calculate_distance_matrix()

    def calculate_distance_matrix(self):
        n = len(self.delivery_requests) + 1
        self.distance_matrix = np.zeros((n, n))
        for i, delivery1 in enumerate(self.delivery_requests):
            self.distance_matrix[0, i + 1] = self.station.distance(delivery1.start) + delivery1.distance
            self.distance_matrix[i + 1, 0] = delivery1.end.distance(self.station)
            for j, delivery2 in enumerate(self.delivery_requests):
                self.distance_matrix[i + 1, j + 1] = delivery1.end.distance(delivery2.start) + delivery2.distance

    def generate_drones_tasks(self, count=DEFAULT_DRONE_COUNT, generations=1000):
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

        self.drones_tasks = [[x - 1 for i, x in enumerate(d) if i] for d in best_solution]
        print(self.drones_tasks)

    def random_solution(self, count=DEFAULT_DRONE_COUNT):
        delivery_indexes = np.arange(1, len(self.delivery_requests) + 1)
        np.random.shuffle(delivery_indexes)
        random_drones = np.random.randint(count, size=(len(delivery_indexes)))
        solution = [[0] for _ in range(count)]

        for drone, delivery_idx in zip(random_drones, delivery_indexes):
            solution[drone].append(delivery_idx)

        return solution

    def calculate_total_distance(self, paths):
        return np.sum(self.distance_matrix[paths[:-1], paths[1:]])
