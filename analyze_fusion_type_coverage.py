import pandas as pd
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

def save_insights_to_file(insights, file_name="type_effectiveness_insights.xlsx"):
    """
    Save all insights into an Excel file.

    Args:
    - insights (dict): Insights generated from the effectiveness data.
    - file_name (str): Name of the file to save the results.
    """
    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
        for insight_name, insight_data in insights.items():
            # Convert the data to a DataFrame if not already one
            if isinstance(insight_data, pd.DataFrame):
                insight_data.to_excel(writer, sheet_name=insight_name)
            else:
                # Convert to DataFrame for non-DataFrame insights
                df = pd.DataFrame(insight_data)
                df.to_excel(writer, sheet_name=insight_name)

    print(f"Insights have been written to {file_name}")

def calculate_advanced_insights(effectiveness_data):
    """
    Calculate additional insights for attack combinations.

    Args:
    - effectiveness_data (DataFrame): Effectiveness probabilities for attack combinations.

    Returns:
    - insights (dict): Insights including highest x2+ damage, neutral types, resistances, and other metrics.
    """
    insights = {}

    # Calculate percentage of x2 or higher damage
    effectiveness_data["x2_or_higher"] = (
        effectiveness_data["Super Effective (x4)"].fillna(0) +
        effectiveness_data["Super Effective (x2)"].fillna(0)
    )

    # Calculate Net Advantage Score
    effectiveness_data["net_advantage"] = (
        effectiveness_data["Super Effective (x4)"] * 4 +
        effectiveness_data["Super Effective (x2)"] * 2 -
        effectiveness_data["Resisted (x1/2)"] * 0.5 -
        effectiveness_data["Resisted (x1/4)"] * 0.25 -
        effectiveness_data["Immune"] * 1
    )

    # Calculate Neutral Coverage (Neutral + x2 + x4)
    effectiveness_data["neutral_coverage"] = (
        effectiveness_data["Neutral"].fillna(0) +
        effectiveness_data["Super Effective (x2)"].fillna(0) +
        effectiveness_data["Super Effective (x4)"].fillna(0)
    )

    # Calculate Resistance Score
    effectiveness_data["resistance_score"] = (
        effectiveness_data["Resisted (x1/2)"].fillna(0) +
        effectiveness_data["Resisted (x1/4)"].fillna(0) +
        effectiveness_data["Immune"].fillna(0)
    )

    # Calculate Weakness Exposure
    effectiveness_data["weakness_exposure"] = effectiveness_data["resistance_score"]

    # Calculate Consistency (low standard deviation implies high consistency)
    effectiveness_data["consistency"] = 1 / effectiveness_data[
        ["Neutral", "Super Effective (x2)", "Super Effective (x4)", "Resisted (x1/2)", "Resisted (x1/4)", "Immune"]
    ].std(axis=1).fillna(1)  # Avoid divide-by-zero

    # Find attack combinations with the highest percentage of x2 or higher
    insights["highest_x2_or_higher"] = effectiveness_data.sort_values(
        by="x2_or_higher", ascending=False
    ).head(171)

    # Find attack combinations with the highest percentage of Neutral damage
    insights["highest_neutral"] = effectiveness_data.sort_values(
        by="Neutral", ascending=False
    ).head(171)

    # Find combinations with the least resistances
    insights["least_resistances"] = effectiveness_data.sort_values(
        by="resistance_score", ascending=True
    ).head(171)

    # Find attack combinations with the highest Neutral Coverage
    insights["highest_neutral_coverage"] = effectiveness_data.sort_values(
        by="neutral_coverage", ascending=False
    ).head(171)

    # Find attack combinations with the best Net Advantage
    insights["highest_net_advantage"] = effectiveness_data.sort_values(
        by="net_advantage", ascending=False
    ).head(171)

    # Calculate overall worst attack combinations (high Immune or low x2_or_higher)
    effectiveness_data["total_immune_or_resisted"] = effectiveness_data["weakness_exposure"]
    insights["worst_combinations"] = effectiveness_data.sort_values(
        by="total_immune_or_resisted", ascending=False
    ).head(171)

    return insights

def analyze_consistency(effectiveness_file):
    """
    Full analysis pipeline for identifying the most consistent attack combinations.
    """
    # Load data
    effectiveness_data = pd.read_csv(effectiveness_file, index_col=0)

    # Advanced insights
    insights = calculate_advanced_insights(effectiveness_data)

    # Save insights to a file
    save_insights_to_file(insights)

    print("\nInsights have been saved to the output file.")

# Main Execution
if __name__ == "__main__":
    effectiveness_file = "type_coverage_probabilities.csv"
    analyze_consistency(effectiveness_file)

