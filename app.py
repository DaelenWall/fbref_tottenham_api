from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import logging
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/scrape/tottenham_players")
def scrape_tottenham_players():
    url = 'https://fbref.com/en/squads/361ca564/2023-2024/matchlogs/c361ca564/some-player-stats-page'
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        table = soup.find('table', {'id': 'stats_standard_9'})
        if table is None:
            logger.error("⚠️ Player stats table not found on the page!")
            return {"error": "Player stats table not found."}

        headers = [th.getText() for th in table.find('thead').find_all('th')]
        rows = table.find('tbody').find_all('tr')

        player_stats = []
        for row in rows:
            th = row.find('th', {'scope': 'row'})
            td_cells = row.find_all('td')
            if th and td_cells:
                row_data = [th.getText()] + [td.getText() for td in td_cells]
                player_stats.append(row_data)

        # Filter rows to match header length
        player_stats = [row for row in player_stats if len(row) == len(headers)]

        df = pd.DataFrame(player_stats, columns=headers)
        if 'Rk' in df.columns:
            df = df.drop(columns=['Rk'])

        csv_file = 'tottenham_player_stats.csv'
        df.to_csv(csv_file, index=False)
        logger.info("✅ Player data saved to CSV.")

        return {"message": "Player scraping and saving complete.", "rows": len(df)}

    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return {"error": "An error occurred during player scraping."}
