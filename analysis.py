import os

import matplotlib.pyplot as plt
import pandas as pd

from genetic_algorithm.strategies import *
from model import Model


class Analysis:
    DEFAULT_CUSTOMER_COUNT = 12

    def __init__(self):
        np.random.seed(0)
        self.model = Model()

    def run(self, generations, crossover_methods, iterations=10):
        self.generate_problem()

        for crossover_method in crossover_methods:
            results = self.get_results(iterations, generations=generations, crossover_method=crossover_method)
            best_scores, mean_scores, std_scores = zip(
                *(self.calculate_scores_statistics(results, gen) for gen in range(generations)))

            args = range(1, generations + 1), best_scores, mean_scores, std_scores, crossover_method
            self.plot_results(*args)
            self.save_to_file(*args)

    def generate_problem(self, customer_count=DEFAULT_CUSTOMER_COUNT):
        self.model.generate_customers(customer_count)

    def get_results(self, iterations, output=False, **kwargs):
        results = []

        for _ in range(iterations):
            self.model.generate_routes(output=output, show_plot=output, **kwargs)
            results.append(self.model.result)

        return results

    @staticmethod
    def calculate_scores_statistics(results, generation=-1):
        scores = [result.best_scores_history[generation] for result in results]
        return np.min(scores), np.mean(scores), np.std(scores)

    @staticmethod
    def plot_results(generations, best_scores, mean_scores, std_scores, method):
        plt.figure(figsize=(10, 5))
        plt.plot(generations, best_scores, label='Best Score')
        plt.plot(generations, mean_scores, label='Mean Score')
        n = 10  # Display every nth point
        plt.errorbar(generations[::n], mean_scores[::n], yerr=std_scores[::n], fmt='o', label='Std Score', color="C3")
        plt.errorbar(generations[-1], mean_scores[-1], yerr=std_scores[-1], fmt='o', color="C3")
        plt.xlabel('Generation')
        plt.ylabel('Score')
        plt.title(f'Scores vs. Generation ({method.__name__.replace("_", " ")})')
        plt.legend()
        plt.grid(True)
        plt.show()

    @staticmethod
    def save_to_file(generations, best_scores, mean_scores, std_scores, method, directory="analysis_results"):
        os.makedirs(directory, exist_ok=True)
        df = pd.DataFrame({
            "Generation": generations,
            "Best Score": np.round(best_scores, 2),
            "Mean Score": np.round(mean_scores, 2),
            "Std. Score": np.round(std_scores, 2),
        })
        df.to_csv(os.path.join(directory, f"{method.__name__}.csv"), index=False)


if __name__ == "__main__":
    analysis = Analysis()
    analysis.run(800, [order_crossover, order_based_crossover, partially_mapped_crossover, cycle_crossover])
