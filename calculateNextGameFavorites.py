import json


# Load data from JSON files
def load_from_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)


# Save the output to a JSON file
def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


# Load the upcoming games odds and unweighted power rankings
upcoming_games_odds = load_from_file("json/upcoming_games_odds.json")
unweighted_power_ranking = load_from_file("json/unweighted_power_ranking.json")


# Normalize team names for matching
def normalize_team_name(name):
    team_name_mapping = {
        "ARI": "Arizona Cardinals",
        "ATL": "Atlanta Falcons",
        "BAL": "Baltimore Ravens",
        "BUF": "Buffalo Bills",
        "CAR": "Carolina Panthers",
        "CHI": "Chicago Bears",
        "CIN": "Cincinnati Bengals",
        "CLE": "Cleveland Browns",
        "DAL": "Dallas Cowboys",
        "DEN": "Denver Broncos",
        "DET": "Detroit Lions",
        "GB": "Green Bay Packers",
        "HOU": "Houston Texans",
        "IND": "Indianapolis Colts",
        "JAX": "Jacksonville Jaguars",
        "KC": "Kansas City Chiefs",
        "LAC": "Los Angeles Chargers",
        "LAR": "Los Angeles Rams",
        "LV": "Las Vegas Raiders",
        "MIA": "Miami Dolphins",
        "MIN": "Minnesota Vikings",
        "NE": "New England Patriots",
        "NO": "New Orleans Saints",
        "NYG": "New York Giants",
        "NYJ": "New York Jets",
        "PHI": "Philadelphia Eagles",
        "PIT": "Pittsburgh Steelers",
        "SEA": "Seattle Seahawks",
        "SF": "San Francisco 49ers",
        "TB": "Tampa Bay Buccaneers",
        "TEN": "Tennessee Titans",
        "WAS": "Washington Commanders"
    }
    return team_name_mapping.get(name, name)


# List to store the output data
output_data = []

# Iterate through each game in the upcoming games odds
for game in upcoming_games_odds:
    # Normalize team names
    team1_full_name = normalize_team_name(game['odds1'].split()[0])
    team2_full_name = normalize_team_name(game['odds2'].split()[0])

    # Get power rankings and adjust team2's ranking
    team1_ranking = round(unweighted_power_ranking.get(team1_full_name, 0), 3)
    team2_ranking = round(unweighted_power_ranking.get(team2_full_name, 0) * 1.1, 3)

    # Determine the order to store based on which ranking is higher
    if team1_ranking >= team2_ranking:
        game_output = {
            "matchup": f"{game['team1']} (Power Ranking: {team1_ranking}) vs {game['team2']} (Power Ranking: {team2_ranking})",
            "odds": game['odds1']
        }
    else:
        game_output = {
            "matchup": f"{game['team2']} (Power Ranking: {team2_ranking}) vs {game['team1']} (Power Ranking: {team1_ranking})",
            "odds": game['odds2']
        }

     # Determine the order to print based on which ranking is higher
    if team1_ranking >= team2_ranking:
        print(
                f"{game['team1']} (Power Ranking: {team1_ranking}) vs {game['team2']} (Power Ranking: {team2_ranking})")
        print(f"\tOdds: {game['odds1']}")
    else:
        print(
                f"{game['team2']} (Power Ranking: {team2_ranking}) vs {game['team1']} (Power Ranking: {team1_ranking})")
        print(f"\tOdds: {game['odds2']}")

    # Add the game details to the output list
    output_data.append(game_output)

# Save the output data to a JSON file
save_to_file(output_data, "json/output_games_details.json")

