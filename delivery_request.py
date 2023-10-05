from customer import Customer
from point import Point


class DeliveryRequest(Customer):
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

    @staticmethod
    def random():
        start = Point.random()
        end = Point.random()
        while start.distance(end) < DeliveryRequest.MIN_DISTANCE or start.distance(end) > DeliveryRequest.MAX_DISTANCE:
            end = Point.random()
        return DeliveryRequest(start, end)

    def get_coordinates(self):
        return [self.start.x, self.start.y, self.end.x, self.end.y]

    def __str__(self):
        return f"Delivery request: Start {self.start}, End {self.end}, Distance {self.distance_value}"
