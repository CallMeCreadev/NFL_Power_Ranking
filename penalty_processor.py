import json

# Define the mapping of team abbreviations to full team names
team_name_mapping = {
    "Baltimore": "Baltimore Ravens",
    "Kansas City": "Kansas City Chiefs",
    "Philadelphia": "Philadelphia Eagles",
    "Green Bay": "Green Bay Packers",
    "Pittsburgh": "Pittsburgh Steelers",
    "Atlanta": "Atlanta Falcons",
    "Buffalo": "Buffalo Bills",
    "Arizona": "Arizona Cardinals",
    "Tennessee": "Tennessee Titans",
    "Chicago": "Chicago Bears",
    "New England": "New England Patriots",
    "Cincinnati": "Cincinnati Bengals",
    "Houston": "Houston Texans",
    "Indianapolis": "Indianapolis Colts",
    "Miami": "Miami Dolphins",
    "Jacksonville": "Jacksonville Jaguars",
    "New Orleans": "New Orleans Saints",
    "Carolina": "Carolina Panthers",
    "N.Y. Giants": "New York Giants",
    "Minnesota": "Minnesota Vikings",
    "LA Chargers": "Los Angeles Chargers",
    "Las Vegas": "Las Vegas Raiders",
    "Denver": "Denver Broncos",
    "Seattle": "Seattle Seahawks",
    "Dallas": "Dallas Cowboys",
    "Cleveland": "Cleveland Browns",
    "Washington": "Washington Commanders",
    "Tampa Bay": "Tampa Bay Buccaneers",
    "LA Rams": "Los Angeles Rams",
    "Detroit": "Detroit Lions",
    "San Francisco": "San Francisco 49ers",
    "N.Y. Jets": "New York Jets"
}

# Load the data from your file
input_filename = 'normalized_net_yards.json'
with open(input_filename, 'r') as file:
    data = json.load(file)

# Update the team names using the mapping
for team in data:
    original_name = team['team']
    # Replace the team name with the full name if it's in the mapping
    if original_name in team_name_mapping:
        team['team'] = team_name_mapping[original_name]

# Save the updated data to a new JSON file
output_filename = 'json/normalized_penalty_yards.json'
with open(output_filename, 'w') as output_file:
    json.dump(data, output_file, indent=4)

print(f"Updated team names saved to '{output_filename}'.")
