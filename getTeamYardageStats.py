import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json


# Function to scrape offensive yards
def scrape_offensive_yards(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url} (status code: {response.status_code})")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    table_scroller = soup.find('div', class_='Table__Scroller')
    if not table_scroller:
        print("Could not find the scroller div.")
        return None

    table_body = table_scroller.find('tbody', class_='Table__TBODY')
    if not table_body:
        print("Could not find the data table body inside the scroller.")
        return None

    offensive_yards = []

    for row in table_body.find_all('tr', class_='Table__TR'):
        cells = row.find_all('td')
        if len(cells) >= 3:
            yards_value = cells[2].find('div').get_text(strip=True)
            offensive_yards.append(float(yards_value))

    df = pd.DataFrame(offensive_yards, columns=['Offensive Yards'])
    return df


# Function to scrape defensive yards
def scrape_defensive_yards(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url} (status code: {response.status_code})")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    table_scroller = soup.find('div', class_='Table__Scroller')
    if not table_scroller:
        print("Could not find the scroller div.")
        return None

    table_body = table_scroller.find('tbody', class_='Table__TBODY')
    if not table_body:
        print("Could not find the data table body inside the scroller.")
        return None

    defensive_yards = []

    for row in table_body.find_all('tr', class_='Table__TR'):
        cells = row.find_all('td')
        if len(cells) >= 3:
            yards_value = cells[2].find('div').get_text(strip=True)
            defensive_yards.append(float(yards_value))

    df = pd.DataFrame(defensive_yards, columns=['Defensive Yards'])
    return df


# Function to scrape team names
def get_team_names(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url} (status code: {response.status_code})")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    return extract_team_names_from_soup(soup)


def extract_team_names_from_soup(soup):
    # Convert the soup object to a string for regex parsing
    soup_text = str(soup)

    # Define the regex pattern to extract displayName fields
    pattern = r'"displayName":"(.*?)"'

    # Find all matches of the pattern
    team_names = re.findall(pattern, soup_text)

    # Convert the list of team names into a DataFrame
    df = pd.DataFrame(team_names, columns=['Team Names'])
    return df


# Function to save a dictionary to a JSON file
def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")


# Function to load a dictionary from a JSON file
def load_from_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)


# Main function to run the scraper
if __name__ == "__main__":

    NFL_team_names = [
        'Baltimore Ravens', 'Detroit Lions', 'New Orleans Saints',
        'Green Bay Packers', 'San Francisco 49ers', 'Philadelphia Eagles', 'Arizona Cardinals',
        'Miami Dolphins', 'Houston Texans', 'Washington Commanders', 'Minnesota Vikings',
        'Los Angeles Chargers', 'Seattle Seahawks',
        'Indianapolis Colts', 'Kansas City Chiefs', 'Los Angeles Rams', 'Dallas Cowboys', 'Atlanta Falcons',
        'Tampa Bay Buccaneers',
        'New England Patriots', 'Buffalo Bills', 'Jacksonville Jaguars', 'Las Vegas Raiders', 'Cincinnati Bengals',
        'New York Giants',
        'Tennessee Titans', 'New York Jets', 'Cleveland Browns', 'Denver Broncos', 'Pittsburgh Steelers',
        'Chicago Bears', 'Carolina Panthers'
    ]

    # URLs for offensive and defensive stats
    offensive_stats_url = "https://www.espn.com/nfl/stats/team"
    defensive_stats_url = "https://www.espn.com/nfl/stats/team/_/view/defense"

    # Scrape the offensive and defensive stats
    offensive_stats = scrape_offensive_yards(offensive_stats_url)
    defensive_stats = scrape_defensive_yards(defensive_stats_url)
    team_names_offense = get_team_names(offensive_stats_url)  # Assuming team names are from the offensive stats page
    team_names_defense = get_team_names(defensive_stats_url)

    # Filter team names to include only NFL team names
    if team_names_offense is not None:
        team_names_offense = team_names_offense[team_names_offense['Team Names'].isin(NFL_team_names)].reset_index(
            drop=True)

    if team_names_defense is not None:
        team_names_defense = team_names_defense[team_names_defense['Team Names'].isin(NFL_team_names)].reset_index(
            drop=True)

    # Combine team names with their respective stats into dictionaries
    offensive_stats_dict = dict(zip(team_names_offense['Team Names'], offensive_stats['Offensive Yards']))
    defensive_stats_dict = dict(zip(team_names_defense['Team Names'], defensive_stats['Defensive Yards']))

    # Display the combined dictionaries
    print("Offensive Stats Dictionary:")
    print(offensive_stats_dict)

    print("\nDefensive Stats Dictionary:")
    print(defensive_stats_dict)

    # Save the dictionaries to files
    save_to_file(offensive_stats_dict, "json/TeamsOffense.json")
    save_to_file(defensive_stats_dict, "json/TeamsDefense.json")

    # Example of loading the dictionaries back into a Python script
    loaded_offense = load_from_file("json/TeamsOffense.json")
    loaded_defense = load_from_file("json/TeamsDefense.json")

    print("\nLoaded Offensive Stats Data:")
    print(loaded_offense)

    print("\nLoaded Defensive Stats Data:")
    print(loaded_defense)
