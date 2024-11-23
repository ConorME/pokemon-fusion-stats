import itertools
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

types = list(type_chart.keys())

defensive_type_chart = {
        'normal': {'fighting': 2, 'ghost': 0},
        'fire': {'fire': 0.5, 'water': 2, 'grass': 0.5, 'ice': 0.5, 'ground': 2, 'bug': 0.5, 'rock': 2, 'steel': 0.5, 'fairy': 0.5},
        'water': {'fire': 0.5, 'water': 0.5, 'electric': 2, 'grass': 2, 'ice': 0.5, 'steel': 0.5},
        'electric': {'electric': 0.5, 'ground': 2, 'flying': 0.5, 'steel': 0.5},
        'grass': {'fire': 2, 'water': 0.5, 'electric': 0.5, 'grass': 0.5, 'ice': 2, 'poison': 2, 'ground': 0.5, 'flying': 2, 'bug': 2},
        'ice': {'fire': 2, 'ice': 0.5, 'fighting': 2, 'rock': 2, 'steel': 2}, 
        'fighting': {'flying': 2, 'psychic': 2, 'bug': 0.5, 'rock': 0.5, 'dark': 0.5, 'fairy': 2}, 
        'poison': {'grass': 0.5, 'fighting': 0.5, 'poison': 0.5, 'ground': 2, 'psychic': 2, 'bug': 0.5, 'fairy': 0.5},
        'ground': {'water': 2, 'electric': 0, 'grass': 2, 'ice': 2, 'poison': 0.5, 'rock': 0.5}, 
        'flying': {'electric': 2, 'grass': 0.5, 'ice': 2, 'fighting': 0.5, 'ground': 0, 'bug': 0.5, 'rock': 2},
        'psychic': {'fighting': 0.5, 'psychic': 0.5, 'bug': 2, 'ghost': 2, 'dark': 2}, 
        'bug': {'fire': 2, 'grass': 0.5, 'fighting': 0.5, 'ground': 0.5, 'flying': 2, 'rock': 2},
        'rock': {'normal': 0.5, 'fire': 0.5, 'water': 2, 'grass': 2, 'fighting': 2, 'poison': 0.5, 'ground': 2, 'flying': 0.5, 'steel': 2},
        'ghost': {'normal': 0, 'fighting': 0, 'poison': 0.5, 'bug': 0.5, 'ghost': 2, 'dark': 2},
        'dragon': {'fire': 0.5, 'water': 0.5, 'electric': 0.5, 'grass': 0.5, 'ice': 2, 'dragon': 2, 'fairy': 2},
        'dark': {'fighting': 2, 'psychic': 0, 'bug': 2, 'ghost': 0.5, 'dark': 0.5, 'fairy': 2},
        'steel': {'normal': 0.5, 'fire': 2, 'grass': 0.5, 'ice': 0.5, 'fighting': 2, 'poison': 0, 'ground': 2, 'flying': 0.5, 'psychic': 0.5, 'bug': 0.5, 'rock': 0.5, 'dragon': 0.5, 'steel': 0.5, 'fairy': 0.5},
        'fairy': {'fighting': 0.5, 'poison': 2, 'bug': 0.5, 'dragon': 0, 'dark': 0.5, 'steel': 2}
        } 

print(defensive_type_chart)

def calculate_defense(type1, type2):
    resistances, weaknesses, immunities = 0, 0, 0
    for attack_type in type_chart:
        multiplier1 = defensive_type_chart.get(type1, {}).get(attack_type, 1)
        multiplier2 = defensive_type_chart.get(type2, {}).get(attack_type, 1)
        combined_multiplier = min(multiplier1, multiplier2)

        if combined_multiplier < 1:
            resistances += 1
        elif combined_multiplier == 0:
            immunities += 1
        elif combined_multiplier > 1:
            weaknesses += 1

    return resistances, weaknesses, immunities

defensive_results = []
for type1, type2 in itertools.combinations_with_replacement(types, 2):
    resistances, weaknesses, immunities = calculate_defense(type1, type2)
    defensive_score = resistances + immunities - weaknesses
    defensive_results.append({
        "type1": type1, "type2": type2,
        "resistances": resistances, "weaknesses": weaknesses,
        "immunities": immunities, "defensive_score": defensive_score
    })

# Function to calculate offensive coverage for type pairs
def calculate_offense(type1, type2):
    super_effective = 0
    for defense_type in type_chart:
        multiplier1 = type_chart.get(type1, {}).get(defense_type, 1)
        multiplier2 = type_chart.get(type2, {}).get(defense_type, 1)
        combined_multiplier = max(multiplier1, multiplier2)

        if combined_multiplier > 1:
            super_effective += 1

    return super_effective

# Evaluate all type pairs for offense
offensive_results = []
for type1, type2 in itertools.combinations_with_replacement(types, 2):
    super_effective = calculate_offense(type1, type2)
    offensive_results.append({
        "type1": type1, "type2": type2,
        "super_effective": super_effective
    })

# Combine offensive and defensive results
combined_results = []
for defense, offense in zip(defensive_results, offensive_results):
    combined_results.append({
        "type1": defense["type1"],
        "type2": defense["type2"],
        "resistances": defense["resistances"],
        "weaknesses": defense["weaknesses"],
        "immunities": defense["immunities"],
        "defensive_score": defense["defensive_score"],
        "super_effective": offense["super_effective"],
        "combined_score": defense["defensive_score"] + offense["super_effective"]
    })

# Create DataFrame and rank by combined score
results_df = pd.DataFrame(combined_results).sort_values(by="combined_score", ascending=False)
print(results_df.head(10))  # Top 10 type pairs


