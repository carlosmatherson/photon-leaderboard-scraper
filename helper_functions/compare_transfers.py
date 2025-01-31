#%% Import
import pandas as pd
import os

# comapre addresses between data frames
def compare_transfers(photon_leaderboard_df, transfers_df):


    # a place to store matches
   matches = []

    # for each trader on the photon leader board
   for trader in photon_leaderboard_df['Wallet']:
       
        # and each holder in the list of token holder
      for address in transfers_df['To']:
           
           # check if the address first 3 and last 3 chars match
            if (trader[:3] == address[:3]) and (trader[-3:] == address[-3:]):
               
               # if so, add address to match list
               matches.append(address)
        
   return matches