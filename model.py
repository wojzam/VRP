import time

import numpy as np

from file_manager import *
from genetic_algorithm import GA


class Model:
    DEFAULT_CUSTOMERS_COUNT = 6
    DEFAULT_VEHICLES_COUNT = 3
    DEFAULT_GENERATIONS = 100
    DEFAULT_POP_SIZE = 60
    DEFAULT_PC = 0.7
    DEFAULT_PM = 0.1
    DEFAULT_DISTANCE_FACTOR = 1.
    DEFAULT_TIME_FACTOR = 2.

    customers = []
    targets = []
    routes = []
    distance_matrix = np.empty((0, 0))
    depot = Point(0, 0)

    best_distance = 0
    best_time = 0
    best_score = 0
    execution_time = 0

    def clear_solution(self):
        self.best_distance = 0
        self.best_time = 0
        self.best_score = 0
        self.execution_time = 0
        self.routes = []

    def generate_customers(self, count=DEFAULT_CUSTOMERS_COUNT, customer_type=Customer):
        self.customers = [customer_type.random() for _ in range(count)]
        self.update_targets()

    def update_targets(self):
        self.targets = self.customers[:]
        self.add_depot()
        self.calculate_distance_matrix()
        self.clear_solution()

    def add_depot(self):
        depot_class = Customer if not self.customers else type(self.customers[0])
        self.targets.insert(0, depot_class(self.depot))

    def set_depot_position(self, x, y):
        self.depot.x, self.depot.y = x, y
        self.update_targets()

    def calculate_distance_matrix(self):
        self.distance_matrix = np.zeros((len(self.targets), len(self.targets)))
        for i, target1 in enumerate(self.targets):
            for j, target2 in enumerate(self.targets):
                self.distance_matrix[i, j] = target1.distance(target2)

    def generate_routes(self,
                        vehicles_count=DEFAULT_VEHICLES_COUNT,
                        size=DEFAULT_POP_SIZE,
                        generations=DEFAULT_GENERATIONS,
                        pc=DEFAULT_PC,
                        pm=DEFAULT_PM,
                        distance_factor=DEFAULT_DISTANCE_FACTOR,
                        time_factor=DEFAULT_TIME_FACTOR):
        ga = GA(len(self.customers), vehicles_count, distance_factor, time_factor, self.calculate_total_distance)
        st = time.time()
        best_solution, self.best_distance, self.best_time, self.best_score = ga.evolve(size, generations, pc, pm)
        self.execution_time = time.time() - st
        self.calculate_routes_vectors(best_solution)

        print(best_solution)
        print(f"Time:{self.best_time} Distance: {self.best_distance} Score: {self.best_score}"
              f" Execution time: {self.execution_time}")

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

    def save_customers(self, file_path):
        if self.customers:
            write_customers_to_file(self.customers, self.customers[0].COLUMNS, file_path)

    def read_customers(self, file_path):
        self.customers = read_customers_from_file(file_path)
        self.update_targets()
