import math

import numpy as np

from constants import *


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx ** 2 + dy ** 2)

    @classmethod
    def random(cls):
        return cls(np.random.randint(-CANVAS_WIDTH / 2, CANVAS_WIDTH / 2),
                   np.random.randint(-CANVAS_HEIGHT / 2, CANVAS_HEIGHT / 2))

    def __str__(self):
        return f"({self.x}, {self.y})"
