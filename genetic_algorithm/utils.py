import matplotlib.pyplot as plt


def plot_results(global_best_scores, best_scores, mean_scores):
    plt.figure(figsize=(10, 5))
    plt.plot(range(len(global_best_scores)), global_best_scores, label='Global Best Score', marker='o')
    plt.plot(range(len(best_scores)), best_scores, label='Best Score', marker='x')
    plt.plot(range(len(mean_scores)), mean_scores, label='Mean Score', marker='x')
    plt.xlabel('Generation')
    plt.ylabel('Score')
    plt.legend()
    plt.title('Evolution of Best Scores')
    plt.grid(True)
    plt.show()
