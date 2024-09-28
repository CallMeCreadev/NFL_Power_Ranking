import json

# Load the player stats and injury data from JSON files
with open('json/player_rushing.json', 'r') as rushing_file:
    rushing_data = json.load(rushing_file)

with open('json/quarterback_stats.json', 'r') as QB_file:
    QB_data = json.load(QB_file)

with open('json/player_Defense_Stats.json', 'r') as defense_file:
    defense_data = json.load(defense_file)

with open('json/player_receiving.json', 'r') as receiving_file:
    receiving_data = json.load(receiving_file)

with open('json/nfl_injuries.json', 'r') as injuries_file:
    injury_data = json.load(injuries_file)

# Extract player names from the injury data
injured_players = {player["name"] for player in injury_data}

# Prune the data by removing injured players
pruned_rushing_data = {name: stats for name, stats in rushing_data.items() if name not in injured_players}
pruned_QB_data = {name: stats for name, stats in QB_data.items() if name not in injured_players}
pruned_defense_data = {name: stats for name, stats in defense_data.items() if name not in injured_players}
pruned_receiving_data = {name: stats for name, stats in receiving_data.items() if name not in injured_players}

# Save each pruned dataset to its respective JSON file
pruned_rush_filename = 'json/pruned_player_rushing.json'
with open(pruned_rush_filename, 'w') as pruned_rush_file:
    json.dump(pruned_rushing_data, pruned_rush_file, indent=4)

pruned_QB_filename = 'json/pruned_quarterback_stats.json'
with open(pruned_QB_filename, 'w') as pruned_QB_file:
    json.dump(pruned_QB_data, pruned_QB_file, indent=4)

pruned_defense_filename = 'json/pruned_player_Defense_Stats.json'
with open(pruned_defense_filename, 'w') as pruned_defense_file:
    json.dump(pruned_defense_data, pruned_defense_file, indent=4)

pruned_receiving_filename = 'json/pruned_player_receiving.json'
with open(pruned_receiving_filename, 'w') as pruned_receiving_file:
    json.dump(pruned_receiving_data, pruned_receiving_file, indent=4)

print(f"Pruned data saved to {pruned_rush_filename}")
print(f"Pruned data saved to {pruned_QB_filename}")
print(f"Pruned data saved to {pruned_defense_filename}")
print(f"Pruned data saved to {pruned_receiving_filename}")
