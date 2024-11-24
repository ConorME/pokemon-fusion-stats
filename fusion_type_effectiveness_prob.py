import json
import pandas as pd

with open("offensive_type_chart.json", "r") as f:
    type_chart = json.load(f)

pokemon_data = pd.read_csv("pokemon.csv")

pokemon_types = pokemon_data.set_index("name")[["type1", "type2"]].apply(
    lambda row: [row["type1"]] + ([row["type2"]] if not pd.isna(row["type2"]) else []), axis=1
).to_dict()

def calculate_effectiveness(attacking_type, defending_types):
    multiplier = 1
    for defending_type in defending_types:
        if defending_type in type_chart.get(attacking_type, {}):
            multiplier *= type_chart[attacking_type][defending_type]
    if multiplier == 4:
        return "Super Effective (x4)"
    elif multiplier == 2:
        return "Super Effective (x2)"
    elif multiplier < 1 and multiplier > 0.25:
        return "Resisted (x1/2)"
    elif multiplier < 0.25 and multiplier > 0:
        return "Resisted (x1/4)"
    elif multiplier == 0:
        return "Immune"
    else:
        return "Neutral"

results = {attacking_type: {"Super Effective (x4)": 0, "Super Effective (x2)": 0, "Resisted (x1/2)": 0,  "Resisted (x1/4)": 0, "Immune": 0, "Neutral": 0} for attacking_type in type_chart.keys()}

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

with open("type_effectiveness.json", "w") as json_file:
    json.dump(probabilities, json_file, indent=4)

probability_df.to_csv("type_effectiveness_probabilities.csv")

