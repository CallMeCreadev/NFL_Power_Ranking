import subprocess
import os
import time
import sys  # Import sys to access the current Python interpreter


def run_script(script_name, output_file=None, timeout=60):
    # Use the same Python interpreter that is running this script
    python_executable = sys.executable

    result = subprocess.run([python_executable, script_name], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"{script_name} ran successfully.")
        if output_file:
            if not wait_for_file(output_file, timeout):
                print(f"Error: Output file {output_file} was not found.")
                return False  # Stop if output file is missing
    else:
        print(f"Error running {script_name}.")
        print(result.stderr)
        return False  # Stop if the script fails
    return True  # Continue if everything is successful


def wait_for_file(filepath, timeout=60):
    start_time = time.time()
    while not os.path.exists(filepath):
        if time.time() - start_time > timeout:
            print(f"Timeout waiting for file {filepath}")
            return False
        time.sleep(1)
    print(f"File {filepath} is ready.")
    return True


if __name__ == "__main__":

    new_listing_run_scripts_with_output_files = [
        ("getQBStats.py", "json/quarterback_stats.json"),
        ("getDefensiveBigPlays.py", 'json/player_Defense_Stats.json'),
        ("getRecieverStats.py", 'json/player_receiving.json'),
        ("getPlayerRushing.py", 'json/player_rushing.json'),
        ("getNextGameRoster.py", 'json/nfl_injuries.json'),
        ("prune_injured_players.py", 'json/pruned_player_receiving.json'),
        ("playerStatsProcessor.py", 'json/team_stat_ratios.json'),
        ("getTeamPenaltyStats.py", 'json/penalty_yards_data.json'),
        ("penalty_processor.py", 'json/normalized_penalty_yards.json'),
        ("getTeamYardageStats.py", "json/TeamsDefense.json"),
        ("getTeamMatchHistory.py", "json/ScoresByTeam.json"),
        ("getPowerRanking.py", 'json/unweighted_power_ranking.json'),
        ("getNextWeeksGames.py", 'upcoming_games_odds.json')
    ]

    for script, output_file in new_listing_run_scripts_with_output_files:
        if not run_script(script, output_file):
            print("Stopping execution due to an error.")
            break

    cleanup_script = "FileCleanup.py"

    run_script(cleanup_script)
