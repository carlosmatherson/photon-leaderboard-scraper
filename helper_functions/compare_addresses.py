#%% Import
import pandas as pd
import os

# comapre addresses between data frames
def compare_addresses(photon_leaderboard_df, token_holders_df):


    # a place to store matches
   matches = []
   trader_check = []
   holder_check = []


    # for each trader on the photon leader board
   for trader in photon_leaderboard_df['Wallet']:
       
        # and each holder in the list of token holder
      for holder in token_holders_df['Account']:
           
           # check if the address first 3 and last 3 chars match
            if (trader[:3] == holder [:3]) and (trader[-3:] == holder[-3:]):
               
               # if so, add address to match list
               matches.append(holder)

            holder_check.append(f'{holder[:3]}..{holder[-3:]}')

      trader_check.append(f'{trader}')
            
        
   return matches, trader_check, holder_check