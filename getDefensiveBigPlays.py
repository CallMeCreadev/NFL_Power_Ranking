from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import json

# Set up WebDriver
driver = webdriver.Chrome()  # Ensure your ChromeDriver is installed and in PATH
url = "https://www.espn.com/nfl/stats/player/_/view/defense/table/defensive/sort/sacks/dir/desc"
driver.get(url)

# Function to click "Show More" button until it's no longer available
def click_show_more(driver):
    try:
        show_more = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.AnchorLink.loadMore__link"))
        )
        show_more.click()
        time.sleep(2)  # Wait for content to load
        return True
    except TimeoutException:
        print("No more 'Show More' button found or timed out.")
        return False

# Click "Show More" until it disappears
while click_show_more(driver):
    pass

# Get the page source after all data is loaded
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Get the first <tbody> containing player names and teams
name_team_body = soup.find_all('tbody', class_='Table__TBODY')[0]

# Get the second <tbody> containing the stats
stats_body = soup.find_all('tbody', class_='Table__TBODY')[1]

# Dictionary to store player information
players_dict = {}

# Extract player names and teams from the first <tbody>
for row in name_team_body.find_all('tr', class_='Table__TR'):
    player_cell = row.find('td', class_='Table__TD')
    if player_cell:
        player_info = player_cell.find_next('td')
        player_name = player_info.find('a').text
        team_name = player_info.find('span', class_='athleteCell__teamAbbrev').text
        players_dict[player_name] = {'Team': team_name}

# Function to get ratings from the second <tbody>
def getAVG_rush(row):
    td_elements = row.find_all('td', class_='Table__TD')
    if len(td_elements) >= 14:
        rating1 = td_elements[5].text  # Example: 45.5
        rating2 = td_elements[9].text  # Example: 45.5
        rating3 = td_elements[13].text  # Example: 45.5
        return rating1, rating2, rating3
    return None, None, None

# Extract ratings from the second <tbody> and match them to quarterbacks
idx = 0
for row in stats_body.find_all('tr', class_='Table__TR'):
    rating1, rating2, rating3 = getAVG_rush(row)
    # Use index or other matching criteria if available to ensure correct pairing
    if idx < len(players_dict):
        player_name = list(players_dict.keys())[idx]  # Assuming order matches
        players_dict[player_name]['Sack'] = rating1
        players_dict[player_name]['Int'] = rating2
        players_dict[player_name]['ForcedFumble'] = rating3

        idx += 1

# Function to save the dictionary to a JSON file
def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")

# Save the players_dict to a file
save_to_file(players_dict, 'json/player_Defense_Stats.json')

# Close the WebDriver
driver.quit()
