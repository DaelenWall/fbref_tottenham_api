from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = FastAPI()

@app.get("/scrape/tottenham")
def scrape_tottenham():
    url = 'https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    table = soup.find('table', {'id': 'stats_standard_361ca564'})

    headers = [th.getText() for th in table.find_all('tr')[1].find_all('th')]
    rows = table.find_all('tr')[2:]
    player_stats = []
    for row in rows:
        cells = row.find_all(['th', 'td'])
        player_stats.append([cell.getText() for cell in cells])

    df = pd.DataFrame(player_stats, columns=headers)
    df = df[df['Rk'] != 'Rk']
    df = df.drop(columns=['Rk'])

    # Convert DataFrame to JSON
    result = df.to_dict(orient='records')
    return {"players": result}
