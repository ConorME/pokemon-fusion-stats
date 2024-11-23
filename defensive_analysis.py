import pandas as pd

input_file = "defense_scores.csv"
df = pd.read_csv(input_file)

def top_defensive_combinations(df):
    print(f"\nTop Defensive Combinations by Score:")
    df["defensive_score"] = df["total_resistances"] + df["immunities"] - df["total_weaknesses"]
    top_combinations = df.sort_values(by="defensive_score", ascending=False)
    print(top_combinations)
    return top_combinations

def no_weakness_combinations(df):
    no_weakness = df[df["total_weaknesses"] == 0]
    print(f"\nCombinations with No Weaknesses (Count: {len(no_weakness)}):")
    print(no_weakness)
    return no_weakness

def high_immunity_combinations(df, threshold=2):
    high_immunities = df[df["immunities"] >= threshold]
    print(f"\nCombinations with {threshold} or More Immunities (Count: {len(high_immunities)}):")
    print(high_immunities)
    return high_immunities

def balanced_combinations(df, resistance_threshold=6, weakness_threshold=2):
    balanced = df[(df["total_resistances"] >= resistance_threshold) & (df["total_weaknesses"] <= weakness_threshold)]
    print(f"\nBalanced Combinations (Resistances >= {resistance_threshold} and Weaknesses <= {weakness_threshold}):")
    print(balanced)
    return balanced

def save_results_to_csv(df, results, filename):
    results.to_csv(filename, index=False)
    print(f"Results saved to {filename}")

if __name__ == "__main__":
    print(f"Analyzing {input_file}...\n")

    top_combinations = top_defensive_combinations(df)
    save_results_to_csv(df, top_combinations, "top_defensive_combinations.csv")

    no_weakness = no_weakness_combinations(df)
    save_results_to_csv(df, no_weakness, "no_weakness_combinations.csv")

    high_immunities = high_immunity_combinations(df, threshold=2)
    save_results_to_csv(df, high_immunities, "high_immunity_combinations.csv")

    balanced = balanced_combinations(df, resistance_threshold=6, weakness_threshold=2)
    save_results_to_csv(df, balanced, "balanced_combinations.csv")

