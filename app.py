from fastapi import FastAPI
import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

@app.get("/scrape/tottenham")
def scrape_tottenham():
    url = 'https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats'
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')
        table = soup.find('table', {'id': 'stats_standard_361ca564'})
        if table is None:
            logger.error("⚠️ Stats table not found on the page!")
            return {"error": "Stats table not found."}

        headers = [th.getText() for th in table.find_all('tr')[1].find_all('th')]
        rows = table.find_all('tr')[2:]
        player_stats = []
        for row in rows:
            cells = row.find_all(['th', 'td'])
            player_stats.append([cell.getText() for cell in cells])

        df = pd.DataFrame(player_stats, columns=headers)
        df = df[df['Rk'] != 'Rk']
        df = df.drop(columns=['Rk'])

        result = df.to_dict(orient='records')
        logger.info("✅ Successfully scraped Tottenham data.")
        return {"players": result}

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ HTTP Request failed: {e}")
        return {"error": "Failed to retrieve data."}
    except Exception as e:
        logger.error(f"❌ General error: {e}")
        return {"error": "An error occurred during scraping."}
