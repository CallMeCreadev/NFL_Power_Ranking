import requests
from bs4 import BeautifulSoup
import json


def scrape_match_history(team_url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(team_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve data from {team_url} (status code: {response.status_code})")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the section containing the match history
    schedule_section = soup.find('section', class_='Schedule__Group')
    if not schedule_section:
        print(f"No schedule section found for {team_url}.")
        return []

    match_history = []

    # Find all games within the schedule section
    games = schedule_section.find_all('a', class_='Schedule__Game')

    for game in games:
        # Extract opponent team name
        opponent_tag = game.find('span', class_='Schedule__Team')
        opponent = opponent_tag.get_text(strip=True) if opponent_tag else 'Unknown'

        # Extract game result (e.g., W, L)
        result_tag = game.find('span', class_='Schedule__Result')
        result = result_tag.get_text(strip=True) if result_tag else None

        # Extract score if available
        score_tag = game.find('span', class_='Schedule__Score')
        score = score_tag.get_text(strip=True) if score_tag else 'N/A'

        # Reverse scores if the result is a loss
        if result == 'L' and score != 'N/A':
            # Split the score into individual scores, assume format like '23-20'
            scores = score.split('-')
            if len(scores) == 2:
                # Reverse the score if it's a loss
                score = f"{scores[1]}-{scores[0]}"

        # Only add games with available results
        if result:
            match_history.append({
                'Opponent': opponent,
                'Result': result,
                'Score': score
            })

    return match_history


def fetch_match_history():
    # List of team URLs
    team_urls = [
        "https://www.espn.com/nfl/team/_/name/sf/san-francisco-49ers",
        "https://www.espn.com/nfl/team/_/name/bal/baltimore-ravens",
        "https://www.espn.com/nfl/team/_/name/det/detroit-lions",
        "https://www.espn.com/nfl/team/_/name/no/new-orleans-saints",
        "https://www.espn.com/nfl/team/_/name/gb/green-bay-packers",
        "https://www.espn.com/nfl/team/_/name/phi/philadelphia-eagles",
        "https://www.espn.com/nfl/team/_/name/ari/arizona-cardinals",
        "https://www.espn.com/nfl/team/_/name/mia/miami-dolphins",
        "https://www.espn.com/nfl/team/_/name/hou/houston-texans",
        "https://www.espn.com/nfl/team/_/name/wsh/washington-commanders",
        "https://www.espn.com/nfl/team/_/name/min/minnesota-vikings",
        "https://www.espn.com/nfl/team/_/name/lac/los-angeles-chargers",
        "https://www.espn.com/nfl/team/_/name/sea/seattle-seahawks",
        "https://www.espn.com/nfl/team/_/name/ind/indianapolis-colts",
        "https://www.espn.com/nfl/team/_/name/kc/kansas-city-chiefs",
        "https://www.espn.com/nfl/team/_/name/lar/los-angeles-rams",
        "https://www.espn.com/nfl/team/_/name/atl/atlanta-falcons",
        "https://www.espn.com/nfl/team/_/name/tb/tampa-bay-buccaneers",
        "https://www.espn.com/nfl/team/_/name/ne/new-england-patriots",
        "https://www.espn.com/nfl/team/_/name/buf/buffalo-bills",
        "https://www.espn.com/nfl/team/_/name/jax/jacksonville-jaguars",
        "https://www.espn.com/nfl/team/_/name/lv/las-vegas-raiders",
        "https://www.espn.com/nfl/team/_/name/cin/cincinnati-bengals",
        "https://www.espn.com/nfl/team/_/name/nyg/new-york-giants",
        "https://www.espn.com/nfl/team/_/name/ten/tennessee-titans",
        "https://www.espn.com/nfl/team/_/name/nyj/new-york-jets",
        "https://www.espn.com/nfl/team/_/name/cle/cleveland-browns",
        "https://www.espn.com/nfl/team/_/name/den/denver-broncos",
        "https://www.espn.com/nfl/team/_/name/pit/pittsburgh-steelers",
        "https://www.espn.com/nfl/team/_/name/chi/chicago-bears",
        "https://www.espn.com/nfl/team/_/name/car/carolina-panthers",
        "https://www.espn.com/nfl/team/_/name/dal/dallas-cowboys"
    ]

    # Dictionary to store match histories
    team_match_histories = {}

    # Iterate over each team URL and scrape the match history
    for url in team_urls:
        team_name = url.split('/')[-1].replace('-', ' ').title()
        match_history = scrape_match_history(url)
        if match_history:
            team_match_histories[team_name] = match_history
            print(f"Match history for {team_name} successfully scraped.")
        else:
            print(f"No match history with results found for {team_name}.")

    # Return the collected match histories
    return team_match_histories


def get_opponents_by_team(match_histories):
    opponents_by_team = {}
    scores_for_team = {}  # Separate dictionary to store scores

    for team, games in match_histories.items():
        opponents = [game['Opponent'] for game in games]
        scores = [game['Score'] for game in games]
        opponents_by_team[team] = opponents  # Save only the opponents
        scores_for_team[team] = scores  # Save scores separately

    return opponents_by_team, scores_for_team


def save_to_file(data, filename):
    # Save the data to a JSON file
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")


def load_from_file(filename):
    # Load data from a JSON file
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    # Fetch match history for all teams
    match_histories = fetch_match_history()

    # Get a dictionary of opponents by team and scores separately
    opponents_dict, scores_dict = get_opponents_by_team(match_histories)

    # Save the opponents dictionary to "OpponentsByTeam.json"
    save_to_file(opponents_dict, "json/OpponentsByTeam.json")

    # Save the scores-only dictionary to "ScoresByTeam.json"
    save_to_file(scores_dict, "json/ScoresByTeam.json")

    # Example of loading the dictionary back into a Python script
    loaded_opponents_data = load_from_file("json/OpponentsByTeam.json")
    loaded_scores_data = load_from_file("json/ScoresByTeam.json")

    print("\nLoaded Opponents Data:")
    for team, opponents in loaded_opponents_data.items():
        print(f"{team}: {opponents}")

    print("\nLoaded Scores Data:")
    for team, scores in loaded_scores_data.items():
        print(f"{team}: {scores}")
