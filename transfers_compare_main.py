#%% Import
from helper_functions.photonScraperV2 import scrape_photon_leaderboard_v2
from helper_functions.compare_transfers import compare_transfers
from helper_functions.get_transfers_info import get_transfers_info
from datetime import datetime
import pandas as pd
import os


#%% Paths & timestamp
PHOTON_DATA_PATH = 'photon_leaderboard_captures/'
SOLSCAN_DATA_PATH = 'solscan_transfers_exports/'

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
    transfers_to_df = pd.read_csv(file_path)
    
    FROM = get_transfers_info(file)
    
    matches = compare_transfers(photon_df, transfers_to_df)
    
    result = {
        'TIMESTAMP': timestamp,
        'FROM': FROM,
        'MATCHES': matches
    }

    all_results.append(result)

#%% Update Notes
notes_df = pd.DataFrame(all_results)
notes_df.to_csv(f'transfers_notes/{timestamp}_notes_transfers.csv', index=False)
