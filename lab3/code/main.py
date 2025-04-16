from sat import run_experiment, plot_results
import numpy as np

def main():
    n_values = [10, 50, 100]  # Number of variables
    step = 0.2
    
    k_values = [2]            # K in k-CNF
    T = 100                   # Number of repetitions
    a_values = np.arange(1, 10.1, step)  # Range of a values
    
    for k in k_values:
        for n in n_values:
            print(f"\nRunning experiment with k={k}, n={n}")
            results = run_experiment(n, k, a_values, T)
            plot_results(results, n, k)

if __name__ == "__main__":
    main()