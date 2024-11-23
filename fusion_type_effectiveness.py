import random
import pandas as pd

type_chart = {
    "Normal": {"Rock": 0.5, "Ghost": 0, "Steel": 0.5},
    "Fire": {"Grass": 2, "Ice": 2, "Bug": 2, "Steel": 2, "Fire": 0.5, "Water": 0.5, "Rock": 0.5, "Dragon": 0.5},
    "Water": {"Fire": 2, "Ground": 2, "Rock": 2, "Water": 0.5, "Grass": 0.5, "Dragon": 0.5},
    "Electric": {"Water": 2, "Flying": 2, "Electric": 0.5, "Ground": 0, "Grass": 0.5, "Dragon": 0.5},
    "Grass": {"Water": 2, "Ground": 2, "Rock": 2, "Fire": 0.5, "Grass": 0.5, "Poison": 0.5, "Flying": 0.5, "Bug": 0.5, "Dragon": 0.5, "Steel": 0.5},
    "Ice": {"Grass": 2, "Ground": 2, "Flying": 2, "Dragon": 2, "Fire": 0.5, "Water": 0.5, "Ice": 0.5, "Steel": 0.5},
    "Fighting": {"Normal": 2, "Ice": 2, "Rock": 2, "Dark": 2, "Steel": 2, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Fairy": 0.5, "Ghost": 0},
    "Poison": {"Grass": 2, "Fairy": 2, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0},
    "Ground": {"Fire": 2, "Electric": 2, "Poison": 2, "Rock": 2, "Steel": 2, "Grass": 0.5, "Bug": 0.5, "Flying": 0},
    "Flying": {"Grass": 2, "Fighting": 2, "Bug": 2, "Electric": 0.5, "Rock": 0.5, "Steel": 0.5},
    "Psychic": {"Fighting": 2, "Poison": 2, "Psychic": 0.5, "Steel": 0.5, "Dark": 0},
    "Bug": {"Grass": 2, "Psychic": 2, "Dark": 2, "Fire": 0.5, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Ghost": 0.5, "Steel": 0.5, "Fairy": 0.5},
    "Rock": {"Fire": 2, "Ice": 2, "Flying": 2, "Bug": 2, "Fighting": 0.5, "Ground": 0.5, "Steel": 0.5},
    "Ghost": {"Psychic": 2, "Ghost": 2, "Normal": 0, "Dark": 0.5},
    "Dragon": {"Dragon": 2, "Steel": 0.5, "Fairy": 0},
    "Dark": {"Psychic": 2, "Ghost": 2, "Fighting": 0.5, "Dark": 0.5, "Fairy": 0.5},
    "Steel": {"Ice": 2, "Rock": 2, "Fairy": 2, "Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Steel": 0.5},
    "Fairy": {"Fighting": 2, "Dragon": 2, "Dark": 2, "Fire": 0.5, "Poison": 0.5, "Steel": 0.5}
}

# Example Pokémon and their types
pokemon_types = {
    "Pelipper": ["Water", "Flying"],
    "Ferrothorn": ["Steel", "Grass"],
    "Charizard": ["Fire", "Flying"],
    "Tyranitar": ["Rock", "Dark"],
    # Add more Pokémon as needed...
}

# Function to calculate type effectiveness
def calculate_effectiveness(attacking_type, defending_types):
    multiplier = 1
    for defending_type in defending_types:
        if defending_type in type_chart.get(attacking_type, {}):
            multiplier *= type_chart[attacking_type][defending_type]
    if multiplier > 1:
        return "Super Effective"
    elif multiplier < 1 and multiplier > 0:
        return "Resisted"
    elif multiplier == 0:
        return "Immune"
    else:
        return "Neutral"

# Generate random fusions
def generate_random_fusion(pokemon_list):
    poke1 = random.choice(pokemon_list)
    poke2 = random.choice(pokemon_list)
    return pokemon_types[poke1] + pokemon_types[poke2]

# Initialize results dictionary
results = {attacking_type: {"Super Effective": 0, "Resisted": 0, "Immune": 0, "Neutral": 0} for attacking_type in type_chart.keys()}

# Simulation parameters
num_simulations = 10000
pokemon_list = list(pokemon_types.keys())

# Run simulations
for _ in range(num_simulations):
    fused_types = generate_random_fusion(pokemon_list)
    for attacking_type in type_chart.keys():
        result = calculate_effectiveness(attacking_type, fused_types)
        results[attacking_type][result] += 1

# Convert results to probabilities
probabilities = {
    attack_type: {
        outcome: count / (num_simulations * len(type_chart))
        for outcome, count in outcomes.items()
    }
    for attack_type, outcomes in results.items()
}

# Display results as a DataFrame
probability_df = pd.DataFrame(probabilities).T
print(probability_df)

# Optionally save the results
probability_df.to_csv("type_effectiveness_probabilities.csv")

