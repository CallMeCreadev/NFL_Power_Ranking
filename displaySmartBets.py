import json
import re


# Load data from JSON files
def load_from_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)


# Extract odds from string
def extract_odds(odds_str):
    match = re.search(r'([+-]\d+)', odds_str)
    return int(match.group(1)) if match else 0


# Parse team names and power rankings from the matchup string
def parse_matchup(matchup):
    match = re.findall(r"(.+?) \(Power Ranking: (\d+\.\d+)\)", matchup)
    if match and len(match) == 2:
        team1_name, team1_ranking = match[0]
        team2_name, team2_ranking = match[1]
        return team1_name, float(team1_ranking), team2_name, float(team2_ranking)
    return None, 0, None, 0


# Load game details from JSON file
games_data = load_from_file("json/output_games_details.json")

# Iterate through each game in the JSON data
for game in games_data:
    matchup = game['matchup']
    odds_str = game['odds']

    # Extract team names and power rankings
    team1_name, team1_ranking, team2_name, team2_ranking = parse_matchup(matchup)

    # Check if team 1 power ranking is at least 10% higher than team 2
    if team1_ranking >= team2_ranking * 1.10:
        # Extract the odds
        odds = extract_odds(odds_str)

        # Check if the odds are positive
        if odds > 0:
            # Perform the calculation (team1_ranking / team2_ranking) * odds
            result = (team1_ranking / team2_ranking) * odds

            # If result is greater than 150, print the required details
            if result > 150:
                print(
                    f"{team1_name} (Power Ranking: {team1_ranking}) {team2_name} (Power Ranking: {team2_ranking}), Odds: + {odds}")
