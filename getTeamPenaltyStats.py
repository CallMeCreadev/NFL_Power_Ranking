import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = 'https://www.nflpenalties.com/'

# Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Fetch the page content
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table containing penalty data
table = soup.find('table', class_=['footable', 'footable-loaded'])

# Initialize an empty list to store the net yards data
net_yards_data = []

# Check if the table is found
if table:
    # Find all rows in the table body
    rows = table.find('tbody').find_all('tr')

    # Iterate through each row to extract the Net Yards column (8th column, index 7)
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 7:  # Ensure there are enough columns in the row
            team_name = cells[0].text.strip()  # Optional: Get the team name from the first column
            net_yards = cells[8].text.strip()  # Get the net yards value
            net_yards_data.append({
                "team": team_name,
                "net_yards": net_yards
            })

# Display the scraped Net Yards data
for data in net_yards_data:
    print(f"Team: {data['team']}, Net Yards: {data['net_yards']}")

# Optionally, save the data to a JSON file
import json

with open('json/penalty_yards_data.json', 'w') as file:
    json.dump(net_yards_data, file, indent=4)

print("Net yards data saved to 'net_yards_data.json'.")
