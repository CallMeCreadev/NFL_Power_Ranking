import json
import re


# Function to load a dictionary from a JSON file
def load_from_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)


# Function to normalize team names by converting to lowercase and removing special characters
def normalize_name(name):
    # Convert to lowercase and remove non-alphanumeric characters
    return re.sub(r'\W+', '', name).lower()


# Function to find a matching team name in a dictionary using a normalized name
def find_team_name(team_name, reference_dict):
    normalized_name = normalize_name(team_name)
    for key in reference_dict.keys():
        if normalized_name in normalize_name(key):
            return key
    return None


# Function to calculate the offense calibrated by opponents' average defense
def calculate_offense_oppo_calibrated(offense_dict, defense_dict, opponents_dict):
    offense_oppo_calibrated = {}

    for team, offense_yards in offense_dict.items():
        matched_team = find_team_name(team, opponents_dict)
        if not matched_team:
            print(f"No match found for {team} in opponents dictionary. Skipping calculation.")
            continue

        opponents = opponents_dict.get(matched_team, [])
        if not opponents:
            print(f"No opponents data found for {team}. Skipping calculation.")
            continue

        # Calculate the average defensive yards of the opponents
        opponents_defense_yards = [
            defense_dict.get(find_team_name(opponent, defense_dict), 0)
            for opponent in opponents
            if find_team_name(opponent, defense_dict) is not None
        ]
        if not opponents_defense_yards:
            print(f"No valid defensive data found for opponents of {team}. Skipping calculation.")
            continue

        average_opponent_defense = sum(opponents_defense_yards) / len(opponents_defense_yards)
        offense_oppo_calibrated[team] = offense_yards * (offense_yards / average_opponent_defense)

    return offense_oppo_calibrated


# Function to calculate the defense calibrated by opponents' average offense
def calculate_weak_defense_oppo_calibrated(defense_dict, offense_dict, opponents_dict):
    weak_defense_oppo_calibrated = {}

    for team, defense_yards in defense_dict.items():
        matched_team = find_team_name(team, opponents_dict)
        if not matched_team:
            print(f"No match found for {team} in opponents dictionary. Skipping calculation.")
            continue

        opponents = opponents_dict.get(matched_team, [])
        if not opponents:
            print(f"No opponents data found for {team}. Skipping calculation.")
            continue

        # Calculate the average offensive yards of the opponents
        opponents_offense_yards = [
            offense_dict.get(find_team_name(opponent, offense_dict), 0)
            for opponent in opponents
            if find_team_name(opponent, offense_dict) is not None
        ]
        if not opponents_offense_yards:
            print(f"No valid offensive data found for opponents of {team}. Skipping calculation.")
            continue

        average_opponent_offense = sum(opponents_offense_yards) / len(opponents_offense_yards)
        weak_defense_oppo_calibrated[team] = defense_yards * (defense_yards/average_opponent_offense)

    return weak_defense_oppo_calibrated


# Function to calculate the power rank by dividing offense calibration by defense calibration
def calculate_power_rank(offense_calibrated, weak_defense_calibrated):
    power_ranks = {}

    for team, offense_value in offense_calibrated.items():
        defense_value = weak_defense_calibrated.get(team)
        if defense_value:
            power_ranks[team] = offense_value / defense_value

    # Sort the power ranks in descending order
    sorted_power_ranks = dict(sorted(power_ranks.items(), key=lambda x: x[1], reverse=True))

    return sorted_power_ranks


# Function to group teams into divisions with sorted power ranks
def group_power_ranks_by_division(power_ranks):
    divisions = {
        "AFC East": [
            "Buffalo Bills", "New York Jets", "Miami Dolphins", "New England Patriots"
        ],
        "AFC West": [
            "Kansas City Chiefs", "Los Angeles Chargers", "Las Vegas Raiders", "Denver Broncos"
        ],
        "AFC North": [
            "Baltimore Ravens", "Cincinnati Bengals", "Pittsburgh Steelers", "Cleveland Browns"
        ],
        "AFC South": [
            "Houston Texans", "Jacksonville Jaguars", "Indianapolis Colts", "Tennessee Titans"
        ],
        "NFC East": [
            "Philadelphia Eagles", "Dallas Cowboys", "Washington Commanders", "New York Giants"
        ],
        "NFC West": [
            "San Francisco 49ers", "Seattle Seahawks", "Arizona Cardinals", "Los Angeles Rams"
        ],
        "NFC North": [
            "Detroit Lions", "Minnesota Vikings", "Green Bay Packers", "Chicago Bears"
        ],
        "NFC South": [
            "New Orleans Saints", "Tampa Bay Buccaneers", "Atlanta Falcons", "Carolina Panthers"
        ]
    }

    grouped_power_ranks = {}

    for division, teams in divisions.items():
        division_ranks = {
            team: rank for team, rank in power_ranks.items() if find_team_name(team, {t: None for t in teams})
        }
        grouped_power_ranks[division] = dict(sorted(division_ranks.items(), key=lambda x: x[1], reverse=True))

    return grouped_power_ranks


# Main function to load data and calculate calibrated values
if __name__ == "__main__":
    # Load data from JSON files
    opponents_dict = load_from_file("OpponentsByTeam.json")
    offense_dict = load_from_file("TeamsOffense.json")
    defense_dict = load_from_file("TeamsDefense.json")

    # Calculate offense calibrated by opponents' average defense
    offense_calibrated = calculate_offense_oppo_calibrated(offense_dict, defense_dict, opponents_dict)

    # Calculate weak defense calibrated by opponents' average offense
    weak_defense_calibrated = calculate_weak_defense_oppo_calibrated(defense_dict, offense_dict, opponents_dict)

    # Calculate power rank
    power_ranks = calculate_power_rank(offense_calibrated, weak_defense_calibrated)

    # Group power ranks by division
    grouped_power_ranks = group_power_ranks_by_division(power_ranks)

    # Display grouped power ranks
    for division, ranks in grouped_power_ranks.items():
        print(f"\n{division} Power Ranks (Descending Order):")
        for team, rank in ranks.items():
            print(f"{team}: {rank:.2f}")
