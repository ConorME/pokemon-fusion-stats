import json

offensive_type_chart = {
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

# Save to JSON files
with open("offensive_type_chart.json", "w") as f:
    json.dump(offensive_type_chart, f, indent=4)

with open("defensive_type_chart.json", "w") as f:
    json.dump(defensive_type_chart, f, indent=4)

