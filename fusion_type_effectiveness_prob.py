import pandas as pd

type_chart = {
    "normal": {"rock": 0.5, "ghost": 0, "steel": 0.5},
    "fire": {"grass": 2, "ice": 2, "bug": 2, "steel": 2, "fire": 0.5, "water": 0.5, "rock": 0.5, "dragon": 0.5},
    "water": {"fire": 2, "ground": 2, "rock": 2, "water": 0.5, "grass": 0.5, "dragon": 0.5},
    "electric": {"water": 2, "flying": 2, "electric": 0.5, "ground": 0, "grass": 0.5, "dragon": 0.5},
    "grass": {"water": 2, "ground": 2, "rock": 2, "fire": 0.5, "grass": 0.5, "poison": 0.5, "flying": 0.5, "bug": 0.5, "dragon": 0.5, "steel": 0.5},
    "ice": {"grass": 2, "ground": 2, "flying": 2, "dragon": 2, "fire": 0.5, "water": 0.5, "ice": 0.5, "steel": 0.5},
    "fighting": {"normal": 2, "ice": 2, "rock": 2, "dark": 2, "steel": 2, "poison": 0.5, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "fairy": 0.5, "ghost": 0},
    "poison": {"grass": 2, "fairy": 2, "poison": 0.5, "ground": 0.5, "rock": 0.5, "ghost": 0.5, "steel": 0},
    "ground": {"fire": 2, "electric": 2, "poison": 2, "rock": 2, "steel": 2, "grass": 0.5, "bug": 0.5, "flying": 0},
    "flying": {"grass": 2, "fighting": 2, "bug": 2, "electric": 0.5, "rock": 0.5, "steel": 0.5},
    "psychic": {"fighting": 2, "poison": 2, "psychic": 0.5, "steel": 0.5, "dark": 0},
    "bug": {"grass": 2, "psychic": 2, "dark": 2, "fire": 0.5, "fighting": 0.5, "poison": 0.5, "flying": 0.5, "ghost": 0.5, "steel": 0.5, "fairy": 0.5},
    "rock": {"fire": 2, "ice": 2, "flying": 2, "bug": 2, "fighting": 0.5, "ground": 0.5, "steel": 0.5},
    "ghost": {"psychic": 2, "ghost": 2, "normal": 0, "dark": 0.5},
    "dragon": {"dragon": 2, "steel": 0.5, "fairy": 0},
    "dark": {"psychic": 2, "ghost": 2, "fighting": 0.5, "dark": 0.5, "fairy": 0.5},
    "steel": {"ice": 2, "rock": 2, "fairy": 2, "fire": 0.5, "water": 0.5, "electric": 0.5, "steel": 0.5},
    "fairy": {"fighting": 2, "dragon": 2, "dark": 2, "fire": 0.5, "poison": 0.5, "steel": 0.5}
}

pokemon_data = pd.read_csv("pokemon.csv")

pokemon_types = pokemon_data.set_index("name")[["type1", "type2"]].apply(
    lambda row: [row["type1"]] + ([row["type2"]] if not pd.isna(row["type2"]) else []), axis=1
).to_dict()

print(pokemon_types)

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

results = {attacking_type: {"Super Effective": 0, "Resisted": 0, "Immune": 0, "Neutral": 0} for attacking_type in type_chart.keys()}

pokemon_list = list(pokemon_types.keys())
total_fusions = len(pokemon_list) ** 2

for poke1 in pokemon_list:
    for poke2 in pokemon_list:
        fused_types = pokemon_types[poke1] + pokemon_types[poke2]
        for attacking_type in type_chart.keys():
            result = calculate_effectiveness(attacking_type, fused_types)
            results[attacking_type][result] += 1

probabilities = {
    attack_type: {
        outcome: count / total_fusions
        for outcome, count in outcomes.items()
    }
    for attack_type, outcomes in results.items()
}

probability_df = pd.DataFrame(probabilities).T
print(probability_df)

probability_df.to_csv("type_effectiveness_probabilities.csv")

