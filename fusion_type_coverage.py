import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

def load_data(type_chart_file, pokemon_file):
    """
    Load the type chart and Pokémon data.
    """
    with open(type_chart_file, "r") as f:
        type_chart = json.load(f)

    pokemon_data = pd.read_csv(pokemon_file)
    return type_chart, pokemon_data

def count_type_frequencies(pokemon_data):
    """
    Count the frequency of primary and secondary types in a Pokémon dataset.
    """

    # Count occurrences of each type
    primary_type_counts = pokemon_data['type1'].value_counts().to_dict()
    secondary_type_counts = pokemon_data['type2'].value_counts().dropna().to_dict()

    return primary_type_counts, secondary_type_counts
    
def count_fusion_frequencies(primary_type_counts, secondary_type_counts):
    """
    Compute frequencies of all possible type fusions.
    
    Args:
    - primary_type_counts (dict): Counts of Pokémon primary types.
    - secondary_type_counts (dict): Counts of Pokémon secondary types.

    Returns:
    - fusion_counts (defaultdict): Raw counts of type fusions.
    - fusion_probabilities (dict): Probabilities of type fusions.
    """
    def canonical_fusion(type1, type2):
        """
        Return a canonical representation of a type pair.
        """
        if type2 is None:
            return (type1, None)
        return tuple(sorted([type1, type2]))

    # Initialize fusion counts
    fusion_counts = defaultdict(int)

    # Primary-primary combinations
    for type1, count1 in primary_type_counts.items():
        for type2, count2 in primary_type_counts.items():
            fusion_key = canonical_fusion(type1, type2)
            fusion_counts[fusion_key] += count1 * count2

    # Primary-secondary combinations
    for type1, count1 in primary_type_counts.items():
        for type2, count2 in secondary_type_counts.items():
            fusion_key = canonical_fusion(type1, type2)
            fusion_counts[fusion_key] += count1 * count2

    # Secondary-secondary combinations
    for type1, count1 in secondary_type_counts.items():
        for type2, count2 in secondary_type_counts.items():
            fusion_key = canonical_fusion(type1, type2)
            fusion_counts[fusion_key] += count1 * count2

    # Normalize to probabilities
    total_fusions = sum(fusion_counts.values())
    fusion_probabilities = {fusion: count / total_fusions for fusion, count in fusion_counts.items()}

    return fusion_counts, fusion_probabilities

def calculate_effectiveness_outcome(multiplier):
    """
    Map an effectiveness multiplier to an outcome category.
    """
    if multiplier == 4:
        return "Super Effective (x4)"
    elif multiplier == 2:
        return "Super Effective (x2)"
    elif multiplier == 0:
        return "Immune"
    elif multiplier <= 0.25:
        return "Resisted (x1/4)"
    elif multiplier < 1:
        return "Resisted (x1/2)"
    return "Neutral"


def calculate_conditional_probabilities(type_chart, attack_type, defense_types):
    """
    Compute conditional probabilities of each effectiveness outcome
    for a given attack type against a defending type combination.
    """
    type1 = defense_types[0]
    type2 = defense_types[1] if len(defense_types) > 1 else None

    # Compute multipliers from type chart
    multiplier1 = type_chart.get(attack_type, {}).get(type1, 1)
    multiplier2 = type_chart.get(attack_type, {}).get(type2, 1) if type2 else 1

    multiplier = multiplier1 * multiplier2
    
    return calculate_effectiveness_outcome(multiplier)

def calculate_joint_type_probabilities(type_probabilities):
    """
    Calculate joint probabilities of type fusions directly from Pokémon data.
    """
    # Count exact occurrences of each type combination
    fusion_counts = defaultdict(int)
    total_pokemon = len(pokemon_data)

    for _, row in pokemon_data.iterrows():
        type1 = row["type1"]
        type2 = row["type2"] if not pd.isna(row["type2"]) else None
        fusion_key = tuple(sorted([type1, type2]) if type2 else [type1])
        fusion_counts[fusion_key] += 1

    # Normalize to probabilities
    fusion_probabilities = {key: count / total_pokemon for key, count in fusion_counts.items()}
    return fusion_probabilities


def compute_effectiveness_probabilities(type_chart, joint_probabilities):
    """
    Compute the overall probability of each effectiveness outcome for every attacking type combination.

    Args:
    - type_chart (dict): Type effectiveness chart.
    - joint_probabilities (dict): Precomputed joint probabilities of type combinations.

    Returns:
    - results (defaultdict): A dictionary mapping attack type pairs to their effectiveness probabilities.
    """
    results = defaultdict(lambda: defaultdict(float))

    # Iterate over all attacking type combinations
    for attack_type1 in type_chart.keys():
        for attack_type2 in type_chart.keys():
            attack_pair = f"{attack_type1}/{attack_type2}"

            # Iterate over all defending type combinations and their joint probabilities
            for defense_types, joint_prob in joint_probabilities.items():
                # Compute effectiveness for each attack type
                effectiveness1 = calculate_effectiveness(type_chart, attack_type1, defense_types)
                effectiveness2 = calculate_effectiveness(type_chart, attack_type2, defense_types)

                # Choose the better (max) effectiveness for the attack pair
                max_effectiveness = max(effectiveness1, effectiveness2)

                # Categorize the effectiveness outcome
                if max_effectiveness == 4:
                    outcome = "Super Effective (x4)"
                elif max_effectiveness == 2:
                    outcome = "Super Effective (x2)"
                elif max_effectiveness == 0:
                    outcome = "Immune"
                elif max_effectiveness <= 0.25:
                    outcome = "Resisted (x1/4)"
                elif max_effectiveness < 1:
                    outcome = "Resisted (x1/2)"
                else:
                    outcome = "Neutral"

                # Add weighted probability to the results
                results[attack_pair][outcome] += joint_prob

    return results

def analyze_attack_type_pairs(type_chart, fusion_probabilities):
    """
    Analyze type pair coverage for attack type combinations.

    Args:
    - type_chart (dict): Type chart for calculating effectiveness.
    - fusion_probabilities (dict): Probabilities of type combinations for defending Pokémon.

    Returns:
    - coverage (dict): Effectiveness probabilities for each attack type pair.
    """
    coverage = defaultdict(lambda: defaultdict(float))

    # Iterate over all attack type pairs
    for attack_type1 in type_chart.keys():
        for attack_type2 in type_chart.keys():
            attack_pair = f"{attack_type1}/{attack_type2}"

            # Evaluate against all defending Pokémon type combinations
            for defense_types, defense_prob in fusion_probabilities.items():
                # Compute effectiveness of each attack type
                effectiveness1 = calculate_effectiveness(type_chart, attack_type1, defense_types)
                effectiveness2 = calculate_effectiveness(type_chart, attack_type2, defense_types)

                # Choose the better (max) effectiveness for the pair
                max_effectiveness = max(effectiveness1, effectiveness2)

                # Categorize the effectiveness
                if max_effectiveness == 4:
                    outcome = "Super Effective (x4)"
                elif max_effectiveness == 2:
                    outcome = "Super Effective (x2)"
                elif max_effectiveness == 0:
                    outcome = "Immune"
                elif max_effectiveness < 1 and max_effectiveness > 0.25:
                    outcome = "Resisted (x1/2)"
                elif max_effectiveness <= 0.25:
                    outcome = "Resisted (x1/4)"
                else:
                    outcome = "Neutral"

                # Add weighted probability to the coverage
                coverage[attack_pair][outcome] += defense_prob

    return coverage

def calculate_effectiveness(type_chart, attack_type, defense_types):
    """
    Compute the combined effectiveness of an attack type against a defending type combination.

    Args:
    - type_chart (dict): Type effectiveness chart.
    - attack_type (str): The attacking type.
    - defense_types (tuple): The defending type combination (e.g., ('grass', 'water')).

    Returns:
    - float: The combined effectiveness multiplier.
    """
    type1, type2 = defense_types
    multiplier1 = type_chart.get(attack_type, {}).get(type1, 1)
    multiplier2 = type_chart.get(attack_type, {}).get(type2, 1) if type2 else 1
    return multiplier1 * multiplier2


def display_attack_pair_analysis(coverage):
    """
    Display the analysis of attack type pair coverage.

    Args:
    - coverage (dict): Effectiveness probabilities for each attack type pair.
    """
    print("\n=== Attack Type Pair Coverage ===")
    for attack_pair, outcomes in coverage.items():
        print(f"\nAttack Pair: {attack_pair}")
        for outcome, probability in outcomes.items():
            print(f"  {outcome}: {probability:.2%}")
            
def save_results(probabilities, output_file):
    """
    Save the probabilities to a CSV file.
    """
    results_df = pd.DataFrame.from_dict(probabilities, orient="index").fillna(0)
    results_df.to_csv(output_file)
    print(f"Results saved to '{output_file}'")

# Main Execution
if __name__ == "__main__":
    type_chart_file = "offensive_type_chart.json"
    pokemon_file = "pokemon.csv"
    output_file = "type_coverage_probabilities.csv"

    # Load data
    type_chart, pokemon_data = load_data(type_chart_file, pokemon_file)

    # Count type frequencies
    primary_type_counts, secondary_type_counts = count_type_frequencies(pokemon_data)
    
    # Compute fusion frequencies and fusion probabilities
    fusion_type_counts, fusion_probabilities = count_fusion_frequencies(primary_type_counts, secondary_type_counts)
    
    # Compute effectiveness probabilities
    effectiveness_probabilities = analyze_attack_type_pairs(type_chart, fusion_probabilities)
    
    display_attack_pair_analysis(effectiveness_probabilities)
    
    # Save results
    save_results(effectiveness_probabilities, output_file)
