from customer import Customer
from point import Point


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
