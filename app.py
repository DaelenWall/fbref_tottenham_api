import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI

app = FastAPI()

@app.get("/scrape/tottenham_all_tables")
def scrape_ton_tables():
    url = "https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    # Make sure data/ directory exists
    os.makedirs('data', exist_ok=True)

    # List of table IDs to scrape (excluding match logs)
    table_ids = [
        'stats_standard_9',
        'stats_keeper_9',
        'stats_keeper_adv_9',
        'stats_shooting_9',
        'stats_passing_9',
        'stats_passing_types_9',
        'stats_gca_9',
        'stats_defense_9',
        'stats_possession_9',
        'stats_playing_time_9',
        'stats_misc_9'
    ]

    results = {}

    for table_id in table_ids:
        table = soup.find('table', {'id': table_id})
        if table is None:
            print(f"⚠ Table {table_id} not found, skipping.")
            results[table_id] = "not found"
            continue

        headers = [th.getText() for th in table.find('thead').find_all('th')]
        rows = table.find('tbody').find_all('tr')

        table_data = []
        for row in rows:
            if row.find('th', {'scope': 'row'}) is None:
                continue
            th = row.find('th', {'scope': 'row'})
            td_cells = row.find_all('td')
            row_data = [th.getText()] + [td.getText() for td in td_cells]
            if len(row_data) == len(headers):
                table_data.append(row_data)
            else:
                print(f"⚠ Skipping row in {table_id} — length mismatch.")

        df = pd.DataFrame(table_data, columns=headers)

        # Save to CSV inside data folder
        csv_file = f"data/{table_id}.csv"
        df.to_csv(csv_file, index=False)
        print(f"✅ Saved {table_id} → {csv_file}")
        results[table_id] = f"{len(df)} rows saved"

    return {"message": "Scraping complete", "results": results}
