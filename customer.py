from point import Point


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
