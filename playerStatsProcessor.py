import json
from collections import defaultdict


# Function to load a JSON file into a dictionary
def load_json_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


# Function to aggregate stats by team, summing for each stat category except those specified for averaging
def aggregate_stats_by_team(player_stats, stat_fields, avg_fields=None):
    team_stats = defaultdict(lambda: defaultdict(float))
    team_player_counts = defaultdict(lambda: defaultdict(int))

    avg_fields = avg_fields if avg_fields else []

    for player, stats in player_stats.items():
        team = stats['Team']
        if len(team) < 6:  # Filter out invalid teams
            for stat in stat_fields:
                if stat in stats:
                    team_stats[team][stat] += float(stats[stat])
                    if stat in avg_fields:
                        team_player_counts[team][stat] += 1

    # Calculate the average for specified fields
    for team, stats in team_stats.items():
        for stat in avg_fields:
            if team_player_counts[team][stat] > 0:
                stats[stat] /= team_player_counts[team][stat]  # Compute the average

    return team_stats


# Function to calculate averages for each stat category
def calculate_averages(team_stats, stat_fields):
    averages = defaultdict(float)
    total_teams = 32  # Assuming 32 teams in the league

    for stat in stat_fields:
        total = sum(stats[stat] for stats in team_stats.values() if stat in stats)
        averages[stat] = total / total_teams

    return averages


# Function to convert stats into ratios based on averages
def convert_to_ratios(team_stats, averages):
    ratios = defaultdict(lambda: defaultdict(float))

    for team, stats in team_stats.items():
        for stat, value in stats.items():
            if stat in averages and averages[stat] != 0:
                ratios[team][stat] = value / averages[stat]

    return ratios


# Function to replace team abbreviations with full names
def convert_team_names(final_dict, team_mapping):
    converted_dict = {}
    for abbrev, stats in final_dict.items():
        full_name = team_mapping.get(abbrev)
        if full_name:
            converted_dict[full_name] = stats
        else:
            print(f"Warning: No full name found for abbreviation '{abbrev}'")
    return converted_dict

# Main function to load JSON files, process stats, calculate averages, and convert to ratios
def process_all_stats():
    # Load player stats from JSON files
    defense_stats = load_json_file('json/player_Defense_Stats.json')
    receiving_stats = load_json_file('json/player_receiving.json')
    rushing_stats = load_json_file('json/player_rushing.json')
    qb_stats = load_json_file('json/quarterback_stats.json')

    # Define the stat fields to sum or average for each category
    defense_fields = ['Sack', 'Int', 'ForcedFumble']
    receiving_fields = ['BigPlay', 'Fumble', 'YAC']
    rushing_fields = ['RushAVG', 'BigPlay', 'Fumble']
    qb_fields = ['QBR', 'RTG']

    # Define fields that should be averaged instead of summed
    avg_rushing_fields = ['RushAVG']
    avg_qb_fields = ['QBR', 'RTG']

    # Aggregate stats by team
    defense_team_stats = aggregate_stats_by_team(defense_stats, defense_fields)
    receiving_team_stats = aggregate_stats_by_team(receiving_stats, receiving_fields)
    rushing_team_stats = aggregate_stats_by_team(rushing_stats, rushing_fields,
                                                 avg_fields=avg_rushing_fields)  # Average RushAVG
    qb_team_stats = aggregate_stats_by_team(qb_stats, qb_fields, avg_fields=avg_qb_fields)  # Average QB stats

    # Combine all stats into a single dictionary
    combined_team_stats = defaultdict(lambda: defaultdict(float))

    # Combine each stat category into the overall stats
    for team, stats in defense_team_stats.items():
        # Calculate Defensive_Stat: Sack as 1, Int as 3, ForcedFumble as 2
        stats['Defensive_Stat'] = stats.get('Sack', 0) + stats.get('Int', 0) * 3 + stats.get('ForcedFumble', 0) * 2

        # Remove the individual defense stats from the final dictionary
        del stats['Sack']
        del stats['Int']
        del stats['ForcedFumble']

        combined_team_stats[team]['Defensive_Stat'] = stats['Defensive_Stat']

    for team, stats in receiving_team_stats.items():
        for stat, value in stats.items():
            combined_team_stats[team][stat] += value

    for team, stats in rushing_team_stats.items():
        for stat, value in stats.items():
            combined_team_stats[team][stat] += value

    # Merge QB stats separately because they are averages, not sums
    for team, stats in qb_team_stats.items():
        for stat, value in stats.items():
            combined_team_stats[team][stat] = value  # Use average instead of sum

    # Calculate QB_combined_stat as the average of QBR and RTG
    for team, stats in combined_team_stats.items():
        if 'QBR' in stats and 'RTG' in stats:
            stats['QB_combined_stat'] = (stats['QBR'] + stats['RTG']) / 2

    # Calculate Run_game_stat as the average of YAC and RushAVG
    for team, stats in combined_team_stats.items():
        yac = stats.get('YAC', 0)
        rush_avg = stats.get('RushAVG', 0)
        if yac > 0 and rush_avg > 0:
            stats['Run_game_stat'] = (yac + rush_avg) / 2

    # Remove individual stats after calculating combined stats
    for team, stats in combined_team_stats.items():
        for stat in ['QBR', 'RTG', 'YAC', 'RushAVG']:
            if stat in stats:
                del stats[stat]

    # Calculate averages for each stat category
    all_stat_fields = ['Defensive_Stat', 'BigPlay', 'Fumble', 'QB_combined_stat', 'Run_game_stat']
    averages = calculate_averages(combined_team_stats, all_stat_fields)

    # Convert stats to ratios relative to the averages
    ratios = convert_to_ratios(combined_team_stats, averages)

    # Invert the Fumble ratio after the ratio calculation and handle zero ratios
    fumble_ratios = [stats['Fumble'] for stats in ratios.values() if 'Fumble' in stats and stats['Fumble'] != 0]
    max_fumble_ratio = max(fumble_ratios) if fumble_ratios else 1  # Default to 1 if no non-zero fumble ratios exist

    for team, stats in ratios.items():
        if 'Fumble' in stats:
            if stats['Fumble'] == 0:
                stats['Fumble'] = max_fumble_ratio  # Set to max non-zero ratio
            else:
                stats['Fumble'] = 1 / stats['Fumble']  # Invert the Fumble ratio



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

    final_team_dict = convert_team_names(ratios, team_name_mapping)

    # Save the final dictionary with ratios to a file
    save_to_file(final_team_dict, 'json/team_stat_ratios.json')
    # Print the ratios for each team
    print("Team Stat Ratios Relative to Averages:")
    for team, stats in final_team_dict.items():
        print(f"Team: {team}")
        for stat, ratio in stats.items():
            print(f"  {stat}: {ratio:.2f}")
        print()


# Save aggregated stats to a JSON file
def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")


# Run the processing function
if __name__ == "__main__":
    process_all_stats()
