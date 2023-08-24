import math
import random


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx ** 2 + dy ** 2)

    @staticmethod
    def random():
        return Point(random.randint(10, 790), random.randint(10, 790))

    def __str__(self):
        return f"({self.x}, {self.y})"
