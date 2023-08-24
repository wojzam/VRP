from point import Point


class DeliveryRequest:
    MIN_DISTANCE = 50
    MAX_DISTANCE = 600

    def __init__(self, x0, y0, x1, y1):
        self.start = Point(x0, y0)
        self.end = Point(x1, y1)
        self.distance = self.start.distance(self.end)

    @staticmethod
    def random():
        start = Point.random()
        end = Point.random()
        while start.distance(end) < DeliveryRequest.MIN_DISTANCE or start.distance(end) > DeliveryRequest.MAX_DISTANCE:
            end = Point.random()
        return DeliveryRequest(start.x, start.y, end.x, end.y)

    def __str__(self):
        return f"Delivery request: Start {self.start}, End {self.end}, Distance {self.distance}"
