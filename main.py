#%% Import
from helper_functions.photonScraper import scrape_photon_leaderboard
from helper_functions.photonScraperV2 import scrape_photon_leaderboard_v2
from helper_functions.compare_addresses import compare_addresses
from helper_functions.get_token_info import get_token_info
from datetime import datetime
import pandas as pd
import os


#%% Paths & timestamp
PHOTON_DATA_PATH = 'photon_leaderboard_captures/'
SOLSCAN_DATA_PATH = 'solscan_holder_exports/'

timestamp = datetime.now().strftime('%Y%m%d')

#%% Update Capture & save file

existing_caputres = [file for file in os.listdir(PHOTON_DATA_PATH) if file.startswith(timestamp)]

if not existing_caputres:
    photon_df = scrape_photon_leaderboard_v2()
    photon_df.to_csv(os.path.join(PHOTON_DATA_PATH, f'{timestamp}_photon_leaderboard.csv'))
else:
    recent_capture = max(existing_caputres)
    photon_df = pd.read_csv(os.path.join(PHOTON_DATA_PATH, recent_capture))

#%% Run Comparisons

solscan_files = [f for f in os.listdir(SOLSCAN_DATA_PATH) if f.endswith('.csv')]

all_results = []

for file in solscan_files:

    file_path = os.path.join(SOLSCAN_DATA_PATH, file)
    token_holders_df = pd.read_csv(file_path)
    
    ticker, contract_address = get_token_info(file)
    
    matches, trader_check, holder_check = compare_addresses(photon_df, token_holders_df)
    
    result = {
        'TIMESTAMP': timestamp,
        'TICKER': ticker,
        'CA': contract_address,
        'MATCHES': matches
    }

    all_results.append(result)

#%% Update Notes
notes_df = pd.DataFrame(all_results)
notes_df.to_csv('notes.csv', index=False)

# #%% check
# trader_check = pd.DataFrame(trader_check).to_csv('trader_check.csv')
# holder_check = pd.DataFrame(holder_check).to_csv('holder_check.csv')