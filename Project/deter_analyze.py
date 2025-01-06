import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

# Load simulation results
data = pd.read_csv("deterministic_monte_carlo_results.csv")

# Group by simulation ID
simulation_groups = data.groupby("Simulation_ID")

# Initialize a PDF for combined output
with PdfPages("combined_output.pdf") as pdf:
    
    # Summary table
    summary_stats = []

    def plot_trajectories(simulation_id, group):
        # Filter columns containing "Generation" and ensure correct format
        generation_columns = [col for col in group.columns if col.startswith("Generation_")]

        # Extract generation indices
        generations = [int(col.split("_")[1]) for col in generation_columns]

        # Extract deterministic and Monte Carlo data
        monte_carlo_data = group[generation_columns].T
        deterministic_trajectory = monte_carlo_data.mean(axis=1)

        # Create plot
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=generations, y=deterministic_trajectory, label="Deterministic")
        for col in monte_carlo_data.columns:
            plt.plot(generations, monte_carlo_data[col], alpha=0.2, color="gray")

        plt.xlabel("Generations")
        plt.ylabel("Allele Frequency")
        plt.title(f"Simulation ID {simulation_id}: Trajectories")
        plt.legend()
        plt.tight_layout()

        # Save the plot to the PDF
        pdf.savefig()
        plt.close()

    for sim_id, group in simulation_groups:
        population_size = group["Population_Size"].iloc[0]
        initial_frequency = group["Initial_Allele_Frequency"].iloc[0]
        generations = group["Generations"].iloc[0]
        mutation_rate = group["Mutation_Rate"].iloc[0]

        # Calculate summary statistics
        final_frequencies = group.iloc[:, 1:generations + 2].mean(axis=0).values
        mean_final_frequency = final_frequencies[-1]
        std_final_frequency = group.iloc[:, 1:generations + 2].std(axis=0).values[-1]

        summary_stats.append({
            "Simulation_ID": sim_id,
            "Population_Size": population_size,
            "Initial_Allele_Frequency": initial_frequency,
            "Generations": generations,
            "Mutation_Rate": mutation_rate,
            "Final_Mean_Allele_Frequency": mean_final_frequency,
            "Final_Std_Allele_Frequency": std_final_frequency,
        })

        # Plot trajectories
        plot_trajectories(sim_id, group)

    # Convert summary statistics to DataFrame
    summary_df = pd.DataFrame(summary_stats)
    summary_df.to_csv("deterministic_summary.csv", index=False)

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
    plt.title("Summary of Final Mean Allele Frequencies")
    plt.legend(title="Population Size")
    plt.tight_layout()
    pdf.savefig()
    plt.close()
