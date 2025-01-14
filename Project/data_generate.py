import numpy as np
import pandas as pd

def generate_input_dataset(sample_size=100):
    """
    Generate input parameters for Wright-Fisher and deterministic simulations with population sizes 
    categorized as small, medium, and large based on effective population size (N_e).

    Parameters:
        sample_size: int - Number of parameter sets to generate.

    Returns:
        DataFrame: Input parameter dataset.
    """
    np.random.seed(42)  # For reproducibility

    # Define population size categories
    n_small = sample_size // 3
    n_medium = sample_size // 3
    n_large = sample_size - (n_small + n_medium)  # Ensure total equals sample_size

    small_population_sizes = np.random.randint(10, 100, size=n_small)  # Small: N_e < 100
    medium_population_sizes = np.random.randint(100, 1000, size=n_medium)  # Medium: 100 <= N_e <= 1000
    large_population_sizes = np.random.randint(1001, 10000, size=n_large)  # Large: N_e > 1000

    # Combine all categories
    population_sizes = np.concatenate([small_population_sizes, medium_population_sizes, large_population_sizes])
    np.random.shuffle(population_sizes)  # Shuffle to randomize order

    # Generate other parameters
    initial_allele_freqs = np.random.uniform(0.1, 0.9, size=sample_size)
    generations = np.random.choice([20, 50, 100], size=sample_size)
    selection_coefficients = np.random.uniform(0.01, 0.1, size=sample_size)
    mutation_rates = np.random.uniform(1e-6, 1e-4, size=sample_size)

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

# Display a preview of the dataset
print(input_dataset.head())
