import json
import itertools
import pandas as pd

with open("defensive_type_chart.json", "r") as f:
    type_chart = json.load(f)

types = list(type_chart.keys())

def calculate_type_combo_multipliers(type1, type2):
    multipliers = {}
    for attack_type in type_chart:
        multiplier1 = type_chart[type1].get(attack_type, 1)
        multiplier2 = type_chart[type2].get(attack_type, 1)
        multipliers[attack_type] = multiplier1 * multiplier2
    return multipliers

type_combo_results = []
for type1, type2 in itertools.combinations_with_replacement(types, 2):
    multipliers = calculate_type_combo_multipliers(type1, type2)
    counts = {
        "x0": sum(1 for m in multipliers.values() if m == 0),
        "x1/4": sum(1 for m in multipliers.values() if m == 0.25),
        "x1/2": sum(1 for m in multipliers.values() if m == 0.5),
        "x1": sum(1 for m in multipliers.values() if m == 1),
        "x2": sum(1 for m in multipliers.values() if m == 2),
        "x4": sum(1 for m in multipliers.values() if m == 4),
    }
    type_combo_results.append({
        "type1": type1,
        "type2": type2,
        **counts,
        "total_resistances": counts["x1/4"] + counts["x1/2"],
        "total_weaknesses": counts["x2"] + counts["x4"],
        "immunities": counts["x0"]
    })

type_combo_df = pd.DataFrame(type_combo_results)

type_combo_df["defensive_score"] = (
    type_combo_df["total_resistances"] + type_combo_df["immunities"] - type_combo_df["total_weaknesses"]
)

output_file = "defense_scores.csv"
defensive_df = pd.DataFrame(type_combo_results)
defensive_df.to_csv(output_file, index=False)

print(type_combo_df.sort_values(by="defensive_score", ascending=False).head(10))

