import matplotlib.pyplot as plt

from genetic_algorithm.strategies import *
from model import Model


class Analysis:
    DEFAULT_CUSTOMER_COUNT = 12

    def __init__(self):
        np.random.seed(0)
        self.model = Model()

    def run(self, generations_range, crossover_methods, iterations=10):
        self.generate_problem()

        for crossover_method in crossover_methods:
            best_scores = []
            mean_scores = []
            std_scores = []

            for generations in generations_range:
                print(f"==== Testing: {self.get_name(crossover_method)} in {generations} generations ===")
                results = self.get_results(iterations, generations=generations, crossover_method=crossover_method)
                best_score, mean_score, std_score = self.retrieve_scores(results)
                best_scores.append(best_score)
                mean_scores.append(mean_score)
                std_scores.append(std_score)

            self.plot_results(generations_range, best_scores, mean_scores, std_scores, self.get_name(crossover_method))

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
    def retrieve_scores(results):
        scores = [result.score for result in results]
        best_score = np.min(scores)
        mean_score = np.mean(scores)
        std_score = np.std(scores)

        print(f"Best Score: {best_score}")
        print(f"Mean Score: {mean_score}")
        print(f"Std. Deviation Score: {std_score}")

        return best_score, mean_score, std_score

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


if __name__ == "__main__":
    analysis = Analysis()
    analysis.run([10, 50, 100, 200, 400],
                 [order_crossover, order_based_crossover, partially_mapped_crossover, cycle_crossover])
