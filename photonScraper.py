#%% Import
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

#%% Request & Scrape
url = "https://photon-sol.tinyastro.io/en/leaderboard"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://photon-sol.tinyastro.io/'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

header_elements = soup.select('.p-lboard__table__th')
column_names = [header.text.strip() for header in header_elements]

data_elements = soup.select('.p-lboard__table__td')
texts = [element.text.strip() for element in data_elements]
rows = [texts[i:i+len(column_names)] for i in range(0, len(texts), len(column_names))]

df = pd.DataFrame(rows, columns=column_names)

#%% Transform Data
df['First'] = df['Wallet'].str[:3]
df['Last'] = df['Wallet'].str[-3:]
#%% Save CSV
current_date = datetime.now().strftime('%Y%m%d')
filename = f'photon_leaderboard_{current_date}.csv'
df.to_csv(filename, index=False)
print(f'Data saved to {filename}')
