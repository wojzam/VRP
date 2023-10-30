import os

import matplotlib.pyplot as plt
import optuna
import pandas as pd

from genetic_algorithm.strategies import *
from model import Model


class Analysis:
    DEFAULT_CUSTOMER_COUNT = 15
    DEFAULT_ITERATIONS = 10

    def __init__(self, seed=0):
        np.random.seed(seed)
        self.model = Model()

    def run(self, generations, crossover_methods, iterations=DEFAULT_ITERATIONS):
        self._generate_problem()
        method_scores = []

        for method in crossover_methods:
            results = self._get_results(iterations, generations=generations, crossover_method=method)
            best_scores, mean_scores, std_scores = zip(
                *(self._calculate_scores_statistics(results, gen) for gen in range(generations)))

            method_scores.append((pretty_name(method), mean_scores))

            self._plot_scores(range(1, generations + 1), best_scores, mean_scores, std_scores, pretty_name(method))
            self._save_to_file(range(1, generations + 1), best_scores, mean_scores, std_scores, method.__name__)

        self._plot_method_comparison(method_scores)

    def optimize_hyperparameters(self, generations, crossover_method, iterations=DEFAULT_ITERATIONS, n_trials=100):
        self._generate_problem()

        def objective(trial):
            pc = trial.suggest_float('pc', 0.3, 0.8)
            pm = trial.suggest_float('pm', 0.01, 0.3)
            results = self._get_results(iterations, generations=generations, pc=pc, pm=pm,
                                        crossover_method=crossover_method)

            best_score, mean_score, std_score = self._calculate_scores_statistics(results)
            return best_score + mean_score

        study = optuna.create_study()
        study.optimize(objective, n_trials=n_trials)

        print(study.best_params)

    def _generate_problem(self, customer_count=DEFAULT_CUSTOMER_COUNT):
        self.model.generate_customers(customer_count)

    def _get_results(self, iterations, output=False, **kwargs):
        results = []

        for _ in range(iterations):
            self.model.generate_routes(output=output, show_plot=output, **kwargs)
            results.append(self.model.result)

        return results

    @staticmethod
    def _calculate_scores_statistics(results, generation=-1):
        scores = [result.best_scores_history[generation] for result in results]
        return np.min(scores), np.mean(scores), np.std(scores)

    @staticmethod
    def measure_crossover_impact(population_size=100, iterations=1000):
        def impact(arr1, arr2):
            return 1.0 - np.mean(arr1 == arr2)

        print("Impact on the offsprings")
        print("|".join(f"{header:^17}" for header in ["p1 - o1", "p1 - o2", "p2 - o1", "p2 - o2", "name"]))
        for crossover in [order_crossover, order_based_crossover, partially_mapped_crossover, cycle_crossover]:
            total_impacts = []

            for _ in range(iterations):
                p1, p2 = np.random.permutation(population_size), np.random.permutation(population_size)
                o1, o2 = crossover(p1, p2)
                total_impacts.append([impact(p1, o1), impact(p1, o2), impact(p2, o1), impact(p2, o2)])

            mean_std = [f'{np.mean(np.array(total_impacts)[:, i]):7.2%} ± {np.std(np.array(total_impacts)[:, i]):6.2%}'
                        for i in range(4)]
            print(" |".join(mean_std), "|", pretty_name(crossover))

    @staticmethod
    def plot_scores_from_file(file):
        generations, best_scores, mean_scores, std_scores = analysis._read_file(file)
        Analysis._plot_scores(generations, best_scores, mean_scores, std_scores, file.replace("_", " "))

    @staticmethod
    def plot_method_comparison_from_files(files):
        method_scores = []

        for file in files:
            generations, best_scores, mean_scores, std_scores = analysis._read_file(file)
            method_scores.append((file, mean_scores))

        if method_scores:
            Analysis._plot_method_comparison(method_scores)

    @staticmethod
    def _plot_scores(generations, best_scores, mean_scores, std_scores, method_name):
        plt.figure(figsize=(10, 5))
        plt.plot(generations, best_scores, label='Best Score')
        plt.plot(generations, mean_scores, label='Mean Score')
        n = len(generations) // 10  # Display every nth point
        plt.errorbar(generations[::n], mean_scores[::n], yerr=std_scores[::n], fmt='o', label='Std Score', color="C3")
        plt.errorbar(generations[-1], mean_scores[-1], yerr=std_scores[-1], fmt='o', color="C3")
        plt.xlabel('Generation')
        plt.ylabel('Score')
        plt.title(f'Scores vs. Generation ({method_name})')
        plt.legend()
        plt.grid(True)
        plt.show()

    @staticmethod
    def _plot_method_comparison(scores_methods):
        plt.figure(figsize=(10, 5))
        for method_name, scores in scores_methods:
            plt.plot(range(1, len(scores) + 1), scores, label=method_name)
        plt.xlabel('Generation')
        plt.ylabel('Mean Score')
        plt.title('Scores mean comparison')
        plt.legend()
        plt.grid(True)
        plt.show()

    @staticmethod
    def _save_to_file(generations, best_scores, mean_scores, std_scores, file_name, directory="analysis_results"):
        os.makedirs(directory, exist_ok=True)
        df = pd.DataFrame({
            "Generation": generations,
            "Best Score": np.round(best_scores, 2),
            "Mean Score": np.round(mean_scores, 2),
            "Std. Score": np.round(std_scores, 2),
        })
        df.to_csv(os.path.join(directory, f"{file_name}.csv"), index=False)

    @staticmethod
    def _read_file(file_name, directory="analysis_results"):
        file_path = os.path.join(directory, f"{file_name}.csv")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file {file_path} not found.")

        df = pd.read_csv(file_path)
        return tuple(df[column].tolist() for column in df.columns)


def pretty_name(crossover_method):
    return crossover_method.__name__.replace("_", " ")


if __name__ == "__main__":
    analysis = Analysis()

    # Example 1
    analysis.run(800,
                 [order_crossover, order_based_crossover, partially_mapped_crossover, cycle_crossover])

    # Example 2
    # analysis.optimize_hyperparameters(500, order_crossover)

    # Example 3
    # analysis.measure_crossover_impact()
