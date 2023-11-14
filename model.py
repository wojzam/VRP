from time import time as measure_time

from customers import *
from genetic_algorithm import GA
from genetic_algorithm.strategies import order_crossover


class Model:
    DEFAULT_CUSTOMERS_COUNT = 6
    DEFAULT_PER_LINE_COUNT = 4
    DEFAULT_LINES_COUNT = 4
    DEFAULT_VEHICLES_COUNT = 3
    DEFAULT_GENERATIONS = 100
    DEFAULT_POP_SIZE = 60
    DEFAULT_PC = 0.7
    DEFAULT_PM = 0.1
    DEFAULT_DISTANCE_FACTOR = 1.
    DEFAULT_TIME_FACTOR = 1.
    DEFAULT_CROSSOVER_METHOD = order_crossover

    customers = []
    targets = []
    distance_matrix = np.empty((0, 0))
    depot = Point(0, 0)

    def __init__(self):
        self.result_history = ResultHistory()

    def generate_customers(self, count=DEFAULT_CUSTOMERS_COUNT, customer_class=Customer):
        self.customers = [customer_class.random() for _ in range(count)]
        self.update_targets()

    def generate_customers_along_the_lines(self, per_line_count=DEFAULT_PER_LINE_COUNT,
                                           lines_count=DEFAULT_LINES_COUNT, scale=100):
        angles = 2 * np.pi * np.arange(lines_count) / lines_count
        cos_values, sin_values = np.cos(angles), np.sin(angles)

        alphas = scale * (np.arange(per_line_count) + 1) / per_line_count
        point_x = np.round(cos_values[:, np.newaxis] * alphas).flatten().astype(int)
        point_y = np.round(sin_values[:, np.newaxis] * alphas).flatten().astype(int)

        self.customers = [Customer(Point(x, y)) for x, y in zip(point_x, point_y)]
        self.update_targets()

    def update_targets(self):
        self.targets = self.customers[:]
        self.add_depot()
        self.calculate_distance_matrix()
        self.result_history.clear()

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
                        time_factor=DEFAULT_TIME_FACTOR,
                        crossover_method=DEFAULT_CROSSOVER_METHOD,
                        output=True,
                        show_plot=True):
        try:
            ga = GA(len(self.customers), vehicles_count, distance_factor, time_factor, self.calculate_total_distance)
            start_time = measure_time()
            solution, distance, time, score, best_scores_history = ga.evolve(size, generations, pc, pm,
                                                                             crossover_method, show_plot)
            exec_time = measure_time() - start_time

            self.result_history.add(
                Result(self.calculate_routes_vectors(solution), distance, time, score, best_scores_history, exec_time))

            if output:
                print("Solution: ", solution)
                print(f"Time:{time} Distance: {distance} Score: {score} Execution time: {exec_time}")
        except ValueError as e:
            print(f"ValueError: {e}")

    def calculate_routes_vectors(self, solution):
        routes = []
        for route in solution:
            vectors = []
            for i in range(1, len(route)):
                current = self.targets[route[i]]
                previous = self.targets[route[i - 1]]
                vectors.extend(previous.get_vectors_to(current))
            routes.append(vectors)
        return routes

    def calculate_total_distance(self, routes):
        return np.sum(self.distance_matrix[routes[:-1], routes[1:]])

    def save_customers(self, file_path):
        if self.customers:
            write_customers_to_file(self.customers, self.customers[0].COLUMNS, file_path)

    def read_customers(self, file_path):
        self.customers = read_customers_from_file(file_path)
        self.update_targets()

    @property
    def result(self):
        return self.result_history.get_current()

    def get_pagination_indicator(self):
        return f"{self.result_history.current_index + 1}/{len(self.result_history.results)}"


class Result:

    def __init__(self, routes=None, distance=0., time=0., score=0., best_scores_history=None, execution_time=0.):
        self.routes = routes if routes is not None else []
        self.distance = distance
        self.time = time
        self.score = score
        self.best_scores_history = best_scores_history if best_scores_history is not None else []
        self.execution_time = execution_time


class ResultHistory:
    results = []
    current_index = 0

    def clear(self):
        self.results = []
        self.current_index = 0

    def navigate(self, index_change):
        new_index = self.current_index + index_change
        if 0 <= new_index < len(self.results):
            self.current_index = new_index

    def add(self, result):
        self.results.append(result)
        self.current_index = len(self.results) - 1

    def get_current(self):
        if not self.results:
            return None
        return self.results[self.current_index]
