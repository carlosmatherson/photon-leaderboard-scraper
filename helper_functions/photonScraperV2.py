import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def scrape_photon_leaderboard_v2(num_pages=5):
    base_url = "https://photon-sol.tinyastro.io/en/leaderboard"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cache-Control': 'max-age=0',
        'Cookie': 'session=random_session_id',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    session = requests.Session()
    session.headers.update(headers)
    all_data = []

    for page in range(1, num_pages + 1):
        url = f"{base_url}?page={page}"
        
        try:
            # Random delay between requests
            time.sleep(random.uniform(2, 5))
            
            response = session.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            cells = soup.select('.p-lboard__table__td')
            
            if cells:
                rows = [cells[i:i+4] for i in range(0, len(cells), 4)]
                for row in rows:
                    if len(row) >= 2:
                        rank = row[0].text.strip()
                        wallet = row[1].text.strip()
                        all_data.append([rank, wallet])
                        
        except Exception as e:
            print(f"Error on page {page}: {e}")

    if all_data:
        df = pd.DataFrame(all_data, columns=['Ranking', 'Wallet'])
        df['First'] = df['Wallet'].str[:3]
        df['Last'] = df['Wallet'].str[-3:]
        return df
    
    return pd.DataFrame(columns=['Ranking', 'Wallet', 'First', 'Last'])