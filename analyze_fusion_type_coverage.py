import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("stab_type_combination_effectiveness_optimized.csv")

df.columns = [col.strip() for col in df.columns]

def rank_type_combinations(df):
    """Rank type combinations by offensive potential (x4 + x2)."""
    df["offensive_score"] = df["Super Effective (x4)"] + df["Super Effective (x2)"]
    ranked = df.sort_values(by="offensive_score", ascending=False)
    return ranked

def find_top_performers(df, n=10):
    """Find the top N type combinations with the best offensive scores."""
    ranked = rank_type_combinations(df)
    return ranked.head(n)

def find_bottom_performers(df, n=10):
    """Find the bottom N type combinations based on Neutral and Resisted outcomes."""
    df["neutral_resisted_score"] = df["Neutral"] + df["Resisted (x1/2)"] + df["Resisted (x1/4)"]
    ranked = df.sort_values(by="neutral_resisted_score", ascending=True)
    return ranked.head(n)

def calculate_category_stats(df):
    """Calculate statistical insights for each category."""
    stats = df[[
        "Super Effective (x4)", "Super Effective (x2)", 
        "Resisted (x1/2)", "Resisted (x1/4)", "Immune", "Neutral"
    ]].describe()
    return stats

def plot_category_distribution(df):
    """Visualize category distributions with bar charts."""
    means = df[[
        "Super Effective (x4)", "Super Effective (x2)", 
        "Resisted (x1/2)", "Resisted (x1/4)", "Immune", "Neutral"
    ]].mean()
    means.plot(kind="bar", figsize=(10, 6), title="Average Category Distribution")
    plt.ylabel("Proportion")
    plt.show()

def plot_top_combinations(ranked_df, n=10):
    """Plot the top N type combinations."""
    top_combinations = ranked_df.head(n)
    top_combinations.plot(
        x="type1/type2", y=["Super Effective (x4)", "Super Effective (x2)", "Neutral"],
        kind="bar", figsize=(12, 6), title=f"Top {n} Type Combinations by Offensive Coverage"
    )
    plt.ylabel("Proportion")
    plt.xticks(rotation=45, ha="right")
    plt.show()

print("Category Stats:")
print(calculate_category_stats(df))

top_performers = find_top_performers(df, n=10)
print("\nTop Performers:")
print(top_performers)

bottom_performers = find_bottom_performers(df, n=10)
print("\nBottom Performers:")
print(bottom_performers)

plot_category_distribution(df)
plot_top_combinations(top_performers)

