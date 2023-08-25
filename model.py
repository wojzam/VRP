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

    def generate_drones_tasks(self, count=DEFAULT_DRONE_COUNT):
        delivery_indexes = np.arange(1, len(self.delivery_requests) + 1)
        np.random.shuffle(delivery_indexes)
        random_drones = np.random.randint(count, size=(len(delivery_indexes)))
        solution = [[0] for _ in range(count)]

        for i, drone in enumerate(random_drones):
            solution[drone].append(delivery_indexes[i])

        distances = [self.calculate_total_distance(np.array(drone_paths)) for drone_paths in solution]
        print(sum(distances), distances)

        self.drones_tasks = [[x - 1 for i, x in enumerate(d) if i] for d in solution]
        print(self.drones_tasks)

    def calculate_total_distance(self, paths):
        return np.sum(self.distance_matrix[paths[:-1], paths[1:]])
