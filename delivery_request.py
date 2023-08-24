from point import Point


class DeliveryRequest:
    def __init__(self, x0, y0, x1, y1):
        self.start = Point(x0, y0)
        self.end = Point(x1, y1)
        self.distance = self.start.distance(self.end)

    @staticmethod
    def random():
        start = Point.random()
        end = Point.random()
        return DeliveryRequest(start.x, start.y, end.x, end.y)

    def __str__(self):
        return f"Delivery request: Start {self.start}, End {self.end}, Distance {self.distance}"
