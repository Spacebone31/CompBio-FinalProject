import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

# Load simulation results
data = pd.read_csv("wright_fisher_monte_carlo_simulation_results.csv")

# Group by simulation ID
simulation_groups = data.groupby("Simulation_ID")

# Initialize a PDF for combined output
with PdfPages("wright_fisher_combined_analysis.pdf") as pdf:
    
    # Summary table
    summary_stats = []

    def plot_trajectories(simulation_id, group):
        # Filter columns containing "Generation" and ensure correct format
        generation_columns = [col for col in group.columns if col.startswith("Generation_")]

        # Extract generation indices
        generations = [int(col.split("_")[1]) for col in generation_columns]

        # Extract Monte Carlo data
        monte_carlo_data = group[generation_columns].T
        final_generation = monte_carlo_data.iloc[-1]

        # Create plot
        plt.figure(figsize=(10, 6))
        for col in monte_carlo_data.columns:
            plt.plot(generations, monte_carlo_data[col], alpha=0.2, color="gray")

        plt.xlabel("Generations")
        plt.ylabel("Allele Frequency")
        plt.title(f"Simulation ID {simulation_id}: Wright-Fisher Trajectories")
        plt.tight_layout()

        # Save the plot to the PDF
        pdf.savefig()
        plt.close()

        return final_generation

    for sim_id, group in simulation_groups:
        population_size = group["Population_Size"].iloc[0]
        initial_frequency = group["Initial_Allele_Frequency"].iloc[0]
        generations = group["Generations"].iloc[0]
        mutation_rate = group["Mutation_Rate"].iloc[0]

        # Plot trajectories and get final generation data
        final_frequencies = plot_trajectories(sim_id, group)

        # Calculate summary statistics
        mean_final_frequency = final_frequencies.mean()
        std_final_frequency = final_frequencies.std()

        summary_stats.append({
            "Simulation_ID": sim_id,
            "Population_Size": population_size,
            "Initial_Allele_Frequency": initial_frequency,
            "Generations": generations,
            "Mutation_Rate": mutation_rate,
            "Final_Mean_Allele_Frequency": mean_final_frequency,
            "Final_Std_Allele_Frequency": std_final_frequency,
        })

    # Convert summary statistics to DataFrame
    summary_df = pd.DataFrame(summary_stats)
    summary_df.to_csv("wright_fisher_summary_statistics.csv", index=False)

    # Add summary table to PDF
    plt.figure(figsize=(12, 6))
    plt.axis("off")
    table = plt.table(cellText=summary_df.values, colLabels=summary_df.columns, loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(summary_df.columns))))
    plt.title("Summary Statistics")
    pdf.savefig()
    plt.close()

    # Visualization for summary statistics
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=summary_df, x="Mutation_Rate", y="Final_Mean_Allele_Frequency", hue="Population_Size")
    plt.xlabel("Mutation Rate")
    plt.ylabel("Final Mean Allele Frequency")
    plt.title("Summary of Final Mean Allele Frequencies (Wright-Fisher)")
    plt.legend(title="Population Size")
    plt.tight_layout()
    pdf.savefig()
    plt.close()
