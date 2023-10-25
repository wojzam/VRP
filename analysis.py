import matplotlib.pyplot as plt
from tabulate import tabulate

from genetic_algorithm.strategies import *
from model import Model


class Analysis:
    DEFAULT_CUSTOMER_COUNT = 12

    def __init__(self):
        np.random.seed(0)
        self.model = Model()

    def run(self, generation_range, crossover_methods, iterations=10):
        self.generate_problem()

        for crossover_method in crossover_methods:
            results = self.get_results(iterations, generations=max(generation_range), crossover_method=crossover_method)
            best_scores, mean_scores, std_scores = zip(
                *(self.calculate_scores_statistics(results, gen) for gen in generation_range))

            self.plot_results(generation_range, best_scores, mean_scores, std_scores, self.get_name(crossover_method))
            self.print_table(generation_range, best_scores, mean_scores, std_scores, self.get_name(crossover_method))

    def generate_problem(self, customer_count=DEFAULT_CUSTOMER_COUNT):
        self.model.generate_customers(customer_count)

    def get_results(self, iterations, output=False, **kwargs):
        results = []

        for _ in range(iterations):
            self.model.generate_routes(output=output, show_plot=output, **kwargs)
            results.append(self.model.result)

        return results

    @staticmethod
    def get_name(crossover_method):
        return crossover_method.__name__.replace("_", " ")

    @staticmethod
    def calculate_scores_statistics(results, generation=0):
        scores = [result.best_scores_history[generation - 1] for result in results]
        return np.min(scores), np.mean(scores), np.std(scores)

    @staticmethod
    def plot_results(generations_range, best_scores, mean_scores, std_scores, method_name):
        x_values = range(len(generations_range))
        plt.figure(figsize=(10, 5))
        plt.bar(x_values, best_scores, label='Best Score')
        plt.errorbar(x_values, mean_scores, yerr=std_scores, fmt='o', label='Std Score')
        plt.ylabel('Score')
        plt.title(f'Scores vs. Generations ({method_name})')
        plt.xticks(x_values, [f'{gen} Gen' for gen in generations_range])
        plt.legend()
        plt.grid(True)
        plt.show()

    @staticmethod
    def print_table(generation_range, best_scores, mean_scores, std_scores, method_name):
        data = {
            "Generation": generation_range,
            "Best Score": np.round(best_scores, 2),
            "Mean Score": np.round(mean_scores, 2),
            "Std. Score": np.round(std_scores, 2),
        }
        print(f"\n=== Results for {method_name} ===")
        print(tabulate(data, headers="keys"))


if __name__ == "__main__":
    analysis = Analysis()
    analysis.run([10, 50, 100, 200, 500],
                 [order_crossover, order_based_crossover, partially_mapped_crossover, cycle_crossover])
