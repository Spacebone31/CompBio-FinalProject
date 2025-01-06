import numpy as np
import pandas as pd

def generate_input_dataset(sample_size=100):
    """
    Generate input parameters for Wright-Fisher and deterministic simulations.

    Parameters:
        sample_size: int - Number of parameter sets to generate.

    Returns:
        DataFrame: Input parameter dataset.
    """
    np.random.seed(42)  # For reproducibility

    # Generate parameters
    population_sizes = np.random.choice([50, 100, 500, 1000], size=sample_size)
    initial_allele_freqs = np.random.uniform(0.1, 0.9, size=sample_size)
    generations = np.random.choice([20, 50, 100], size=sample_size)
    selection_coefficients = np.random.uniform(0.01, 0.1, size=sample_size)
    mutation_rates = np.random.uniform(1e-6, 1e-4, size=sample_size)  # Mutation rates typically range from 10^-6 to 10^-4

    # Create DataFrame
    dataset = pd.DataFrame({
        "Population_Size": population_sizes,
        "Initial_Allele_Frequency": initial_allele_freqs,
        "Generations": generations,
        "Selection_Coefficient": selection_coefficients,
        "Mutation_Rate": mutation_rates
    })

    return dataset

# Generate input dataset
input_dataset = generate_input_dataset(sample_size=100)

# Save to CSV
input_dataset.to_csv("input_parameters.csv", index=False)