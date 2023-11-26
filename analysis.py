import os

import matplotlib.pyplot as plt
import pandas as pd

from genetic_algorithm.strategies import *
from model import Model


class Analysis:
    GENERATIONS = 100
    TEST_ITERATIONS = 10
    RESULTS_DIRECTORY = "analysis_results"
    ALL_CROSSOVER_METHODS = [order_crossover, order_based_crossover, position_based_crossover,
                             partially_mapped_crossover, cycle_crossover, edge_recombination_crossover]

    def __init__(self, customer_count=15):
        self.model = Model()
        self.customer_count = customer_count

    def analyse_crossovers(self, crossover_methods, iterations=TEST_ITERATIONS, generations=GENERATIONS, **kwargs):
        self._generate_problem()
        method_scores = []

        for method in crossover_methods:
            results = self._get_results(iterations, generations=generations, crossover_method=method, **kwargs)
            best_scores, mean_scores, std_scores = zip(
                *(self._calculate_scores_statistics(results, gen) for gen in range(generations + 1)))

            method_scores.append((pretty_name(method), mean_scores))

            self._plot_scores(range(generations + 1), best_scores, mean_scores, std_scores, pretty_name(method))
            self._save_to_file({
                "Generation": range(generations + 1),
                "Best Score": best_scores,
                "Mean Score": mean_scores,
                "Std. Score": std_scores},
                method.__name__)

        self._plot_method_comparison(method_scores)

    def analyse_pc_impact(self, crossover_methods, iterations=TEST_ITERATIONS, generations=GENERATIONS, **kwargs):
        self._generate_problem()
        probabilities = np.arange(0.0, 1.0, 0.1)
        method_final_scores = []

        for method in crossover_methods:
            mean_final_scores = []

            for pc in probabilities:
                results = self._get_results(iterations, generations=generations, crossover_method=method, pc=pc,
                                            **kwargs)
                best_score, mean_score, std_score = self._calculate_scores_statistics(results)
                mean_final_scores.append(mean_score)

            method_final_scores.append((pretty_name(method), mean_final_scores))
            self._save_to_file({"PC": probabilities, "Mean score": mean_final_scores}, method.__name__)

        self._plot_pc_method_comparison(probabilities, method_final_scores)

    def _generate_problem(self):
        self.model.generate_customers(self.customer_count)

    def _get_results(self, iterations, output=False, **kwargs):
        results = []

        for i in range(iterations):
            np.random.seed(i)
            self.model.generate_routes(output=output, show_plot=output, **kwargs)
            results.append(self.model.result)

        return results

    @staticmethod
    def _calculate_scores_statistics(results, generation=-1):
        scores = [result.best_scores_history[generation] for result in results]
        return np.min(scores), np.mean(scores), np.std(scores)

    @staticmethod
    def analyse_crossover_impact_on_offsprings(population_size=100, iterations=1000):
        def impact(arr1, arr2):
            return 1.0 - np.mean(arr1 == arr2)

        print("Impact on the offsprings")
        print("|".join(f"{header:^17}" for header in ["p1 - o1", "p1 - o2", "p2 - o1", "p2 - o2", "name"]))
        for crossover in Analysis.ALL_CROSSOVER_METHODS:
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
    def plot_pc_method_comparison_from_files(files):
        method_final_scores = []
        probabilities = []

        for file in files:
            probabilities, mean_scores = analysis._read_file(file)
            method_final_scores.append((file, mean_scores))

        if method_final_scores:
            Analysis._plot_pc_method_comparison(probabilities, method_final_scores)

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
    def _plot_method_comparison(method_scores):
        plt.figure(figsize=(10, 5))
        for method_name, scores in method_scores:
            plt.plot(range(1, len(scores) + 1), scores, label=method_name)
        plt.xlabel('Generation')
        plt.ylabel('Mean Score')
        plt.title('Scores mean comparison')
        plt.legend()
        plt.grid(True)
        plt.show()

    @staticmethod
    def _plot_pc_method_comparison(probabilities, method_final_scores):
        plt.figure(figsize=(10, 5))
        for method_name, scores in method_final_scores:
            plt.plot(probabilities, scores, label=method_name)
        plt.xlabel('Crossover probability')
        plt.ylabel('Mean score')
        plt.title(f'Scores vs. Pc')
        plt.legend()
        plt.grid(True)
        plt.show()

    @staticmethod
    def _save_to_file(dictionary, file_name, directory=RESULTS_DIRECTORY):
        os.makedirs(directory, exist_ok=True)
        pd.DataFrame(dictionary).round(2).to_csv(os.path.join(directory, f"{file_name}.csv"), index=False)

    @staticmethod
    def _read_file(file_name, directory=RESULTS_DIRECTORY):
        file_path = os.path.join(directory, f"{file_name}.csv")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file {file_path} not found.")

        df = pd.read_csv(file_path)
        return tuple(df[column].tolist() for column in df.columns)


def pretty_name(crossover_method):
    return crossover_method.__name__.replace("_", " ")


if __name__ == "__main__":
    analysis = Analysis()
    analyzed_crossover_methods = [order_crossover, order_based_crossover, partially_mapped_crossover, cycle_crossover]
    file_names = [method.__name__ for method in analyzed_crossover_methods]

    # Example 1
    # analysis.analyse_crossovers(analyzed_crossover_methods, generations=50)
    # analysis.plot_method_comparison_from_files(file_names)

    # Example 2
    # analysis.analyse_pc_impact(analyzed_crossover_methods, generations=500)
    # analysis.plot_pc_method_comparison_from_files(file_names)

    # Example 3
    # analysis.analyse_crossover_impact_on_offsprings()


