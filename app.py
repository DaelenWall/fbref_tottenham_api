import pandas as pd
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()

@app.get("/scrape/tottenham_players")
def scrape_tottenham_players():
    url = "https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    # Find all tables and pick the right one by id
    table = soup.find('table', {'id': 'stats_standard_9'})
    if table is None:
        print("⚠ Player stats table not found on the page!")
        return {"error": "Player stats table not found."}

    # Get all column names from 'data-stat' attributes
    headers = [th.get('data-stat') for th in table.find('thead').find_all('th')]

    # Collect player rows as dictionaries
    player_stats = []
    rows = table.find('tbody').find_all('tr')
    for row in rows:
        if row.get('class') and 'thead' in row.get('class'):
            continue  # skip header rows inside tbody

        row_data = {}
        cells = row.find_all(['th', 'td'])

        for header, cell in zip(headers, cells):
            text = cell.get_text(strip=True)
            row_data[header] = text

        player_stats.append(row_data)

    # Convert to DataFrame
    df = pd.DataFrame(player_stats)

    # Optional: clean up or convert columns (example: drop empty rows)
    df = df.dropna(how='all')

    # Save to CSV
    csv_file = 'tottenham_players_data.csv'
    df.to_csv(csv_file, index=False)

    print(f"✅ Player data saved to {csv_file}")
    return {"message": "Player scraping and saving complete.", "rows": len(df)}
