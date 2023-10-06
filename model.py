import numpy as np

from constants import *
from customer import Customer
from genetic_algorithm import GA
from point import Point


class Model:
    DEFAULT_CUSTOMERS_COUNT = 6
    DEFAULT_VEHICLES_COUNT = 3
    DEFAULT_GENERATIONS = 100
    DEFAULT_POP_SIZE = 60

    customers = []
    targets = []
    routes = []
    distance_matrix = np.empty((0, 0))
    depot = Point(CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)

    best_distance = 0
    best_time = 0

    def __init__(self):
        self.ga = GA(self.calculate_total_distance)

    def clear_solution(self):
        self.best_distance = 0
        self.best_time = 0
        self.routes = []

    def generate_targets(self, count=DEFAULT_CUSTOMERS_COUNT, customer_type=Customer):
        self.customers = [customer_type.random() for _ in range(count)]
        self.targets = self.customers[:]
        self.targets.insert(0, customer_type(self.depot))  # Add depot
        self.calculate_distance_matrix()
        self.clear_solution()

    def calculate_distance_matrix(self):
        self.distance_matrix = np.zeros((len(self.targets), len(self.targets)))
        for i, target1 in enumerate(self.targets):
            for j, target2 in enumerate(self.targets):
                self.distance_matrix[i, j] = target1.distance(target2)

    def generate_routes(self,
                        vehicles_count=DEFAULT_VEHICLES_COUNT,
                        size=DEFAULT_POP_SIZE,
                        generations=DEFAULT_GENERATIONS):
        self.ga.set_parameters(len(self.customers), vehicles_count)
        best_solution, self.best_distance, self.best_time = self.ga.evolve(size, generations)

        self.calculate_routes_vectors(best_solution)

        print(best_solution)
        print(self.best_time)
        print(self.best_distance)

    def calculate_routes_vectors(self, solution):
        self.routes = []
        for route in solution:
            vectors = []
            for i in range(1, len(route)):
                current = self.targets[route[i]]
                previous = self.targets[route[i - 1]]
                vectors.extend(previous.get_vectors_to(current))

            self.routes.append(vectors)

    def calculate_total_distance(self, routes):
        return np.sum(self.distance_matrix[routes[:-1], routes[1:]])
