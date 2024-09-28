import requests
from bs4 import BeautifulSoup
import json

# URL of the page to scrape
url = 'https://www.espn.com/nfl/injuries'

# Headers to mimic a request from a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Fetch the page content with headers
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all injury tables for each team
teams = soup.find_all('div', class_=['ResponsiveTable', 'Table__league-injuries'])

injury_data = []

# Iterate through each team's injury table
for team in teams:
    try:
        # Extract the team name
        team_name = team.find('span', class_='injuries__teamName').text.strip()

        # Find all player rows
        players = team.find_all('tr', class_='Table__TR--sm')

        # Iterate through each player to extract data
        for player in players:
            name = player.find('td', class_='col-name').text.strip()
            pos = player.find('td', class_='col-pos').text.strip()
            return_date = player.find('td', class_='col-date').text.strip()
            status = player.find('td', class_='col-stat').text.strip()
            comment = player.find('td', class_='col-desc').text.strip()

            injury_data.append({
                'team': team_name,
                'name': name,
                'position': pos,
                'return_date': return_date,
                'status': status,
                'comment': comment
            })
    except AttributeError:
        print("Could not parse injury details for one of the elements.")

# Save the data to a JSON file
with open('json/nfl_injuries.json', 'w') as json_file:
    json.dump(injury_data, json_file, indent=4)

print("Injury data saved to 'nfl_injuries.json'")
