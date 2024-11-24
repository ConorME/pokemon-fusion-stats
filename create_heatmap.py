import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def plot_heatmap(effectiveness_data, metric, title):
    """
    Plot a heatmap for a selected metric in the effectiveness data.

    Args:
    - effectiveness_data (DataFrame): Effectiveness probabilities for attack combinations.
    - metric (str): Column name of the metric to visualize (e.g., 'Neutral', 'Super Effective (x2)').
    - title (str): Title for the heatmap.

    Returns:
    - None
    """
    # Reset index to separate type combinations
    effectiveness_data = effectiveness_data.reset_index()
    
    # Split type combination into type1 and type2 for pivot table
    effectiveness_data[['type1', 'type2']] = effectiveness_data['index'].str.split('/', expand=True)

    # Pivot the data for the heatmap
    heatmap_data = effectiveness_data.pivot_table(
        index='type1', columns='type2', values=metric, fill_value=0
    )

    # Create the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="YlGnBu", cbar=True)

    # Add titles and labels
    plt.title(title, fontsize=16)
    plt.xlabel("Type 2")
    plt.ylabel("Type 1")
    plt.tight_layout()
    plt.show()

# Example Usage
if __name__ == "__main__":
    # Load data
    effectiveness_file = "type_coverage_probabilities.csv"
    effectiveness_data = pd.read_csv(effectiveness_file, index_col=0)

    # Plot heatmaps for different metrics
    plot_heatmap(effectiveness_data, "Neutral", "Heatmap of Neutral Effectiveness")
    plot_heatmap(effectiveness_data, "Super Effective (x2)", "Heatmap of Super Effective (x2) Effectiveness")
    plot_heatmap(effectiveness_data, "Immune", "Heatmap of Immunity Effectiveness")

