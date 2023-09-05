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

    @staticmethod
    def random():
        return Point(np.random.randint(CANVAS_MARGIN, CANVAS_WIDTH - CANVAS_MARGIN),
                     np.random.randint(CANVAS_MARGIN, CANVAS_HEIGHT - CANVAS_MARGIN))

    def __str__(self):
        return f"({self.x}, {self.y})"
