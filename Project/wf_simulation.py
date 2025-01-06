import numpy as np
import pandas as pd

def wright_fisher_with_mutation(N, p0, generations, u, replicates):
    """
    Wright-Fisher simulation with mutation.

    Parameters:
        N: int - Population size.
        p0: float - Initial allele frequency.
        generations: int - Number of generations to simulate.
        u: float - Mutation rate per generation.
        replicates: int - Number of Monte Carlo replicates.

    Returns:
        DataFrame: Simulated allele frequencies for each replicate.
    """
    results = []

    for rep in range(replicates):
        p = p0
        frequencies = [p]
        for _ in range(generations):
            # Mutation effect
            p = (1 - u) * p + u * (1 - p)
            
            # Wright-Fisher sampling
            k = np.random.binomial(N, p)
            p = k / N
            frequencies.append(p)
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

    # Simulate
    simulation_result = wright_fisher_with_mutation(N, p0, generations, u, replicates)

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
final_results.to_csv("wright_fisher_monte_carlo_simulation_results.csv", index=False)
print("All simulations complete. Results saved to 'combined_simulation_results.csv'.")
