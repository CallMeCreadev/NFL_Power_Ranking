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

# Function to convert dictionary values to float
def convert_dict_values_to_float(d):
    for key in d.keys():
        try:
            d[key] = float(d[key])
        except ValueError:
            print(f"Cannot convert value {d[key]} for key {key} to float.")
            d[key] = 0.0

# Function to calculate average points earned and given for each team
def calculate_average_points(scores_dict):
    average_points_dict = {}
    for team, scores in scores_dict.items():
        points_earned = []
        points_given = []
        for score in scores:
            try:
                earned, given = map(int, score.split('-'))
                points_earned.append(earned)
                points_given.append(given)
            except ValueError:
                print(f"Invalid score format for {team}: {score}. Skipping this score.")
                continue
        if points_earned and points_given:
            average_earned = sum(points_earned) / len(points_earned)
            average_given = sum(points_given) / len(points_given)
            average_points_dict[team] = {'average_earned': average_earned, 'average_given': average_given}
    return average_points_dict

# Function to calculate the offense calibrated by opponents' average defense
def calculate_offense_oppo_calibrated(offense_dict, defense_dict, opponents_dict):
    offense_oppo_calibrated = {}

    for team in offense_dict:
        offense_yards = offense_dict[team]
        matched_team = find_team_name(team, opponents_dict)
        if not matched_team:
            print(f"No match found for {team} in opponents dictionary. Skipping calculation.")
            continue

        opponents = opponents_dict.get(matched_team, [])
        if not opponents:
            print(f"No opponents data found for {team}. Skipping calculation.")
            continue

        # Calculate the average defensive yards of the opponents
        opponents_defense_yards = []
        for opponent in opponents:
            matched_opponent = find_team_name(opponent, defense_dict)
            if matched_opponent:
                opponent_defense = defense_dict[matched_opponent]
                opponents_defense_yards.append(opponent_defense)
        if not opponents_defense_yards:
            print(f"No valid defensive data found for opponents of {team}. Skipping calculation.")
            continue

        average_opponent_defense = sum(opponents_defense_yards) / len(opponents_defense_yards)
        offense_oppo_calibrated[team] = offense_yards * (offense_yards / average_opponent_defense)

    return offense_oppo_calibrated

# Function to calculate the defense calibrated by opponents' average offense
def calculate_weak_defense_oppo_calibrated(defense_dict, offense_dict, opponents_dict):
    weak_defense_oppo_calibrated = {}

    for team in defense_dict:
        defense_yards = defense_dict[team]
        matched_team = find_team_name(team, opponents_dict)
        if not matched_team:
            print(f"No match found for {team} in opponents dictionary. Skipping calculation.")
            continue

        opponents = opponents_dict.get(matched_team, [])
        if not opponents:
            print(f"No opponents data found for {team}. Skipping calculation.")
            continue

        # Calculate the average offensive yards of the opponents
        opponents_offense_yards = []
        for opponent in opponents:
            matched_opponent = find_team_name(opponent, offense_dict)
            if matched_opponent:
                opponent_offense = offense_dict[matched_opponent]
                opponents_offense_yards.append(opponent_offense)
        if not opponents_offense_yards:
            print(f"No valid offensive data found for opponents of {team}. Skipping calculation.")
            continue

        average_opponent_offense = sum(opponents_offense_yards) / len(opponents_offense_yards)
        weak_defense_oppo_calibrated[team] = defense_yards * (defense_yards / average_opponent_offense)

    return weak_defense_oppo_calibrated

# Function to calculate points earned calibrated by opponents' average points given
def calculate_points_earned_oppo_calibrated(average_points_dict, opponents_dict):
    points_earned_oppo_calibrated = {}

    for team in average_points_dict:
        average_earned = average_points_dict[team]['average_earned']
        matched_team = find_team_name(team, opponents_dict)
        if not matched_team:
            print(f"No match found for {team} in opponents dictionary. Skipping calculation.")
            continue
        opponents = opponents_dict.get(matched_team, [])
        if not opponents:
            print(f"No opponents data found for {team}. Skipping calculation.")
            continue
        opponents_average_points_given = []
        for opponent in opponents:
            matched_opponent = find_team_name(opponent, average_points_dict)
            if matched_opponent:
                opponent_average_given = average_points_dict[matched_opponent]['average_given']
                opponents_average_points_given.append(opponent_average_given)
        if not opponents_average_points_given:
            print(f"No valid points given data found for opponents of {team}. Skipping calculation.")
            continue
        average_opponent_points_given = sum(opponents_average_points_given) / len(opponents_average_points_given)
        points_earned_oppo_calibrated[team] = average_earned * (average_earned / average_opponent_points_given)
    return points_earned_oppo_calibrated

# Function to calculate points given calibrated by opponents' average points earned
def calculate_points_given_oppo_calibrated(average_points_dict, opponents_dict):
    points_given_oppo_calibrated = {}

    for team in average_points_dict:
        average_given = average_points_dict[team]['average_given']
        matched_team = find_team_name(team, opponents_dict)
        if not matched_team:
            print(f"No match found for {team} in opponents dictionary. Skipping calculation.")
            continue
        opponents = opponents_dict.get(matched_team, [])
        if not opponents:
            print(f"No opponents data found for {team}. Skipping calculation.")
            continue
        opponents_average_points_earned = []
        for opponent in opponents:
            matched_opponent = find_team_name(opponent, average_points_dict)
            if matched_opponent:
                opponent_average_earned = average_points_dict[matched_opponent]['average_earned']
                opponents_average_points_earned.append(opponent_average_earned)
        if not opponents_average_points_earned:
            print(f"No valid points earned data found for opponents of {team}. Skipping calculation.")
            continue
        average_opponent_points_earned = sum(opponents_average_points_earned) / len(opponents_average_points_earned)
        points_given_oppo_calibrated[team] = average_given * (average_given / average_opponent_points_earned)
    return points_given_oppo_calibrated

# Function to calculate the power rank by dividing offense calibration by defense calibration
def calculate_power_rank(offense_calibrated, weak_defense_calibrated, points_earned_calibrated, points_given_calibrated):
    power_ranks = {}
    points_power_ranks = {}

    for team, offense_value in offense_calibrated.items():
        defense_value = weak_defense_calibrated.get(team)
        if defense_value:
            power_ranks[team] = offense_value / defense_value

    for team, points_earned_value in points_earned_calibrated.items():
        points_given_value = points_given_calibrated.get(team)
        if points_given_value:
            points_power_ranks[team] = points_earned_value / points_given_value

    # Sort the power ranks in descending order
    sorted_power_ranks = dict(sorted(power_ranks.items(), key=lambda x: x[1], reverse=True))
    sorted_points_power_ranks = dict(sorted(points_power_ranks.items(), key=lambda x: x[1], reverse=True))

    return sorted_power_ranks, sorted_points_power_ranks

# Function to calculate the true power rank by incorporating all stats
def calculate_true_power_rank(power_ranks, points_power_ranks, team_stat_ratios):
    true_power_rank = {}

    for team, yards_power_rank in power_ranks.items():
        if team == "San Francisco 49ers":
            team = "San Francisco 49Ers"
        points_power_rank = points_power_ranks.get(team)
        # Retrieve additional stats from team_stat_ratios
        if team in team_stat_ratios:
            additional_stats = team_stat_ratios[team]
            # Combine all the stats into a single true power rank by averaging
            combined_rank = (
                yards_power_rank +
                points_power_rank +
                additional_stats.get('Defensive_Stat', 0) +
                additional_stats.get('BigPlay', 0) +
                additional_stats.get('Fumble', 0) +
                additional_stats.get('QB_combined_stat', 0) +
                additional_stats.get('Run_game_stat', 0)
            ) / 7.0
            true_power_rank[team] = combined_rank
        else:
            true_power_rank[team] = (yards_power_rank + points_power_rank) / 2.0

    # Sort the power ranks in descending order
    sorted_true_power_ranks = dict(sorted(true_power_rank.items(), key=lambda x: x[1], reverse=True))

    return sorted_true_power_ranks

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
    scores_dict = load_from_file("ScoresByTeam.json")

    # Load the final team stats dictionary with ratios
    team_stat_ratios = load_from_file("team_stat_ratios.json")  # Make sure to adjust this to the correct filename/path

    # Convert offense and defense values to floats
    convert_dict_values_to_float(offense_dict)
    convert_dict_values_to_float(defense_dict)

    # Calculate average points for each team
    average_points_dict = calculate_average_points(scores_dict)

    # Calculate offense calibrated by opponents' average defense
    offense_calibrated = calculate_offense_oppo_calibrated(offense_dict, defense_dict, opponents_dict)

    # Calculate weak defense calibrated by opponents' average offense
    weak_defense_calibrated = calculate_weak_defense_oppo_calibrated(defense_dict, offense_dict, opponents_dict)

    # Calculate points earned calibrated by opponents' average points given
    points_earned_calibrated = calculate_points_earned_oppo_calibrated(average_points_dict, opponents_dict)

    # Calculate points given calibrated by opponents' average points earned
    points_given_calibrated = calculate_points_given_oppo_calibrated(average_points_dict, opponents_dict)

    # Calculate power rank
    power_ranks, points_power_ranks = calculate_power_rank(
        offense_calibrated, weak_defense_calibrated, points_earned_calibrated, points_given_calibrated
    )

    # Calculate the true power rank including all stats from team_stat_ratios
    true_power_ranks = calculate_true_power_rank(power_ranks, points_power_ranks, team_stat_ratios)

    # Group power ranks by division
    grouped_power_ranks = group_power_ranks_by_division(true_power_ranks)

    # Display grouped power ranks
    for division, ranks in grouped_power_ranks.items():
        print(f"\n{division} Power Ranks (Descending Order):")
        for team, rank in ranks.items():
            print(f"{team}: {rank:.2f}")

    # Display overall true power ranks
    print("\nOverall True Power Ranks:")
    for team, score in sorted(true_power_ranks.items(), key=lambda item: item[1], reverse=True):
        print(f"{team:25} {score:.2f}")
