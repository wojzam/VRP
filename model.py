import random

from constants import *
from delivery_request import DeliveryRequest
from point import Point


class Model:
    DEFAULT_DELIVERY_COUNT = 5
    DEFAULT_DRONE_COUNT = 3

    delivery_requests = []
    drones_tasks = []
    station = Point(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)

    def generate_delivery_requests(self, count=DEFAULT_DELIVERY_COUNT):
        self.delivery_requests = [DeliveryRequest.random() for _ in range(count)]

    def generate_drones_tasks(self, count=DEFAULT_DRONE_COUNT):
        delivery_indexes = list(range(len(self.delivery_requests)))
        random.shuffle(delivery_indexes)
        self.drones_tasks = [[] for _ in range(count)]

        for i in delivery_indexes:
            random.choice(self.drones_tasks).append(i)

        total_distance = sum(self.calculate_total_distance(drone) for drone in self.drones_tasks)
        print(self.drones_tasks)
        print(total_distance)

    def calculate_total_distance(self, paths):
        distance = sum(self.delivery_requests[path].distance for path in paths)
        if paths:
            distance += self.delivery_requests[paths[0]].start.distance(self.station)
        return distance
