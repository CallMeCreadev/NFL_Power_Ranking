import os

# List of files to be removed
files_to_remove = [
    'json/quarterback_stats.json',
    'json/player_Defense_Stats.json',
    'json/player_receiving.json',
    'json/player_rushing.json',
    'json/nfl_injuries.json',
    'json/pruned_player_receiving.json',
    'json/pruned_player_Defense_Stats.json',
    'json/pruned_player_rushing.json',
    'json/pruned_quarterback_stats.json',
    'json/OpponentsByTeam.json',
    'json/team_stat_ratios.json',
    'json/penalty_yards_data.json',
    'json/normalized_penalty_yards.json',
    'json/TeamsDefense.json',
    'json/ScoresByTeam.json',
    'json/TeamsOffense.json'
]

def cleanup_json_files():
    for file_path in files_to_remove:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Removed: {file_path}")
            else:
                print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error removing {file_path}: {e}")

if __name__ == "__main__":
    cleanup_json_files()
