import requests
from bs4 import BeautifulSoup
import pandas as pd

# Scrape photon leaderboard and return dataframe
def scrape_photon_leaderboard():

    # target url
    url = "https://photon-sol.tinyastro.io/en/leaderboard"
    
    # headers to mimic browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://photon-sol.tinyastro.io/'
    }

    # make http request to webpage
    response = requests.get(url, headers=headers)

    # parse html using beautiful soup
    soup = BeautifulSoup(response.text, 'html.parser')

    # extract table headers (found header element using inspect element)
    header_elements = soup.select('.p-lboard__table__th')
    column_names = [header.text.strip() for header in header_elements]

    # extract table data (text) (strip removes " " )
    data_elements = soup.select('.p-lboard__table__td')
    texts = [element.text.strip() for element in data_elements]

    # organize data in rows based on number of column (TODO: update so unecesary columns are not added)
    rows = [texts[i:i+len(column_names)] for i in range(0, len(texts), len(column_names))]

    # create data frame
    df = pd.DataFrame(rows, columns=column_names)

    # make new columns for first and last characters of "wallet" column elements
    df['First'] = df['Wallet'].str[:3]
    df['Last'] = df['Wallet'].str[-3:]

    return df
