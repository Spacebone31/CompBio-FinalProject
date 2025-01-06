import numpy as np
import pandas as pd

def deterministic_with_mutation(N, p0, generations, u):
    """
    Deterministic simulation with mutation.

    Parameters:
        N: int - Population size (not directly used in deterministic model).
        p0: float - Initial allele frequency.
        generations: int - Number of generations to simulate.
        u: float - Mutation rate per generation.

    Returns:
        list: Deterministic allele frequencies over generations.
    """
    p = p0
    frequencies = [p]
    for _ in range(generations):
        # Deterministic mutation effect
        p = (1 - u) * p + u * (1 - p)
        frequencies.append(p)
    return frequencies

def monte_carlo_with_deterministic(N, deterministic_trajectory, replicates):
    """
    Monte Carlo simulation using deterministic trajectory as baseline.

    Parameters:
        N: int - Population size.
        deterministic_trajectory: list - Allele frequencies from deterministic model.
        replicates: int - Number of Monte Carlo replicates.

    Returns:
        DataFrame: Simulated allele frequencies for each replicate.
    """
    generations = len(deterministic_trajectory) - 1
    results = []

    for rep in range(replicates):
        frequencies = []
        for gen in range(generations + 1):
            p = deterministic_trajectory[gen]
            k = np.random.binomial(N, p)
            frequencies.append(k / N)
        results.append(frequencies)

    return pd.DataFrame(results, columns=[f"Generation_{i}" for i in range(generations + 1)])

# Load input parameters
dataset = pd.read_csv("input_parameters.csv")

# Simulation parameters
replicates = 100  # Number of Monte Carlo replicates

# Initialize a list to collect all simulation results
all_simulations = []

# Run simulations and collect results
for index, row in dataset.iterrows():
    N = int(row["Population_Size"])
    p0 = row["Initial_Allele_Frequency"]
    generations = int(row["Generations"])
    u = row["Mutation_Rate"]

    # Deterministic simulation
    deterministic_trajectory = deterministic_with_mutation(N, p0, generations, u)

    # Monte Carlo simulation
    simulation_result = monte_carlo_with_deterministic(N, deterministic_trajectory, replicates)

    # Add metadata to the simulation result
    simulation_result["Simulation_ID"] = index
    simulation_result["Population_Size"] = N
    simulation_result["Initial_Allele_Frequency"] = p0
    simulation_result["Generations"] = generations
    simulation_result["Mutation_Rate"] = u

    # Append to the list of all simulations
    all_simulations.append(simulation_result)

# Concatenate all simulation results into a single DataFrame
final_results = pd.concat(all_simulations, ignore_index=True)

# Save to a single CSV file
final_results.to_csv("deterministic_monte_carlo_results.csv", index=False)
print("All simulations complete. Results saved to 'deterministic_monte_carlo_results.csv'.")
