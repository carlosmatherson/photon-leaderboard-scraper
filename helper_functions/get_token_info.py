import os

# get token ticker and contract address (ca)
def get_token_info(filename):

    # get path basename
    base_name = os.path.basename(filename)
    
    # split filename on '_' because I save the snapshots as TICKER_CA_<rest of default filename from solscan>
    ticker = base_name.split('_')[0]
    ca = base_name.split('_')[1]

    return ticker, ca