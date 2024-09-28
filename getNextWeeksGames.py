import requests
from bs4 import BeautifulSoup
import json

# URL of the page to scrape
url = 'https://sports.yahoo.com/nfl/odds/'

# Fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all game elements with the specified classes
games = soup.find_all('div', class_=['PREGAME', 'sixpack'])

game_data = []

# Iterate through each game element to extract team names and odds
for game in games:
    try:
        team1 = game.find('div', class_='sixpack-away-team').find('span', class_='Fw(600)').text.strip()
        team2 = game.find('div', class_='sixpack-home-team').find('span', class_='Fw(600)').text.strip()

        # Extract odds from the specific part of the odds section
        odds_section = game.find('div', class_='sixpack-bet-ODDS_MONEY_LINE')
        odds_line = odds_section.find('div', class_='D(f) Jc(sb) Fz(12px) Fw(600) Mb(8px)')

        # Get the odds values from the relevant spans
        odds1 = odds_line.find_all('span')[0].text.strip()  # Away team odds (team1)
        odds2 = odds_line.find_all('span')[3].text.strip()  # Home team odds (team2)

        game_data.append({
            'team1': team1,
            'odds1': odds1,
            'team2': team2,
            'odds2': odds2
        })
    except AttributeError:
        print("Could not parse game details for one of the elements.")

# Save the data to a JSON file
with open('json/upcoming_games_odds.json', 'w') as json_file:
    json.dump(game_data, json_file, indent=4)

print("Game data saved to 'upcoming_games_odds.json'")
