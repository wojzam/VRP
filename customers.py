import math

import numpy as np


class Point:
    MAX_RANDOM_X = 400
    MAX_RANDOM_Y = 300

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx ** 2 + dy ** 2)

    @classmethod
    def random(cls):
        return cls(np.random.randint(-Point.MAX_RANDOM_X, Point.MAX_RANDOM_X),
                   np.random.randint(-Point.MAX_RANDOM_Y, Point.MAX_RANDOM_Y))

    def __str__(self):
        return f"({self.x}, {self.y})"


class Customer(Point):
    COLUMNS = ["x", "y"]

    def __init__(self, point: Point):
        super().__init__(point.x, point.y)

    def get_vectors_to(self, other):
        return [(Point(self.x, self.y), Point(other.x, other.y))]

    def get_coordinates(self):
        return [self.x, self.y]

    @classmethod
    def random(cls):
        return cls(Point.random())

    def __str__(self):
        return f"Customer({self.x}, {self.y})"


class CustomerPair(Customer):
    COLUMNS = ['startX', 'startY', 'endX', 'endY']
    MIN_DISTANCE = 50
    MAX_DISTANCE = 600

    def __init__(self, start: Point, end: Point = None):
        super().__init__(start)
        self.start = start
        self.end = start if end is None else end
        self.distance_value = start.distance(self.end)

    def distance(self, other):
        return self.end.distance(other.start) + other.distance_value

    def get_vectors_to(self, other):
        return [(other.start, other.end), (self.end, other.start)]

    def get_coordinates(self):
        return [self.start.x, self.start.y, self.end.x, self.end.y]

    @classmethod
    def random(cls):
        start = Point.random()
        end = Point.random()
        while start.distance(end) < CustomerPair.MIN_DISTANCE or start.distance(end) > CustomerPair.MAX_DISTANCE:
            end = Point.random()
        return cls(start, end)

    def __str__(self):
        return f"Customer Pair: Start {self.start}, End {self.end}, Distance {self.distance_value}"
