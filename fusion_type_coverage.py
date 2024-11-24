import json
import pandas as pd
from itertools import product, combinations_with_replacement

with open("offensive_type_chart.json", "r") as f:
    type_chart = json.load(f)

pokemon_data = pd.read_csv("pokemon.csv")

pokemon_types = pokemon_data.set_index("name")[["type1", "type2"]].apply(
    lambda row: [row["type1"]] + ([row["type2"]] if not pd.isna(row["type2"]) else []), axis=1
).to_dict()

pokemon_list = list(pokemon_types.keys())
fusions = [pokemon_types[p1] + pokemon_types[p2] for p1, p2 in product(pokemon_list, repeat=2)]

effectiveness_cache = {}
for attacking_type in type_chart.keys():
    effectiveness_cache[attacking_type] = {}
    for defending_types in fusions:
        multiplier = 1
        for defending_type in defending_types:
            if defending_type in type_chart[attacking_type]:
                multiplier *= type_chart[attacking_type][defending_type]
        if multiplier == 4:
            result = "Super Effective (x4)"
        elif multiplier == 2:
            result = "Super Effective (x2)"
        elif multiplier < 1 and multiplier > 0.25:
            result = "Resisted (x1/2)"
        elif multiplier < 0.25 and multiplier > 0:
            result = "Resisted (x1/4)"
        elif multiplier == 0:
            result = "Immune"
        else:
            result = "Neutral"
        effectiveness_cache[attacking_type][tuple(defending_types)] = result

results = {}
total_fusions = len(fusions)

for type1, type2 in combinations_with_replacement(type_chart.keys(), 2):
    combo_key = f"{type1}/{type2}"
    results[combo_key] = {
        "Super Effective (x4)": 0,
        "Super Effective (x2)": 0,
        "Resisted (x1/2)": 0,
        "Resisted (x1/4)": 0,
        "Immune": 0,
        "Neutral": 0,
    }
    for defending_types in fusions:
        result1 = effectiveness_cache[type1][tuple(defending_types)]
        result2 = effectiveness_cache[type2][tuple(defending_types)]

        combined_result = max(
            ["Neutral", "Resisted (x1/2)", "Resisted (x1/4)", "Immune", "Super Effective (x2)", "Super Effective (x4)"],
            key=lambda r: (result1 == r, result2 == r),
        )

        results[combo_key][combined_result] += 1

probabilities = {
    combo: {
        outcome: count / total_fusions
        for outcome, count in outcomes.items()
    }
    for combo, outcomes in results.items()
}

with open("stab_type_combination_effectiveness_optimized.json", "w") as json_file:
    json.dump(probabilities, json_file, indent=4)

probability_df = pd.DataFrame(probabilities).T
print(probability_df)

probability_df.to_csv("stab_type_combination_effectiveness_optimized.csv")

