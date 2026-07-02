import os
import re
from bs4 import BeautifulSoup
import pandas as pd

# Load the local HTML file
file_path = r"C:\Users\pytho\Documents\nhl\Nhl Hockey _ Historical Betting Odds 2018_2019.html"

with open(file_path, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file.read(), "html.parser")

games_data = []

# Find all table rows containing match information
rows = soup.find_all("tr")

for row in rows:
    # Find the match cell
    match_cell = row.find("td", class_="match") or row.find("td", class_="l2 match")
    if not match_cell:
        continue
    
    # Extract team names and the hyperlink
    a_tag = match_cell.find("a")
    if not a_tag:
        continue
        
    match_text = a_tag.text.strip()
    match_url = a_tag.get("href", "")
    
    # Extract the unique Game ID from the end of the URL
    game_id_match = re.search(r'/(\d+)$', match_url)
    game_id = game_id_match.group(1) if game_id_match else None
    
    # Extract the game time/timestamp if available
    time_span = match_cell.find("span", class_="time")
    timestamp = time_span.get("ts") if time_span else None
    game_time = time_span.text.strip() if time_span else None

    # Gather the odds (1, X, 2 columns)
    odds_cells = row.find_all("td", class_="r")
    if len(odds_cells) >= 3:
        odds_1 = odds_cells[0].text.strip()
        odds_x = odds_cells[1].text.strip()
        odds_2 = odds_cells[2].text.strip()
    else:
        odds_1, odds_x, odds_2 = None, None, None

    # Append row data to the collection
    games_data.append({
        "game_id": game_id,
        "match": match_text,
        "time": game_time,
        "timestamp": timestamp,
        "odds_1": odds_1,
        "odds_x": odds_x,
        "odds_2": odds_2,
        "url": match_url
    })

# Convert to DataFrame
df = pd.DataFrame(games_data)

# Preview the scraped data
print(df.head())

# Optional: Save it directly to a CSV file
df.to_csv("nhl_historical_odds_2018_2019.csv", index=False)