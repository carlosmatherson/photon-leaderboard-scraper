import os

# get token ticker and contract address (ca)
def get_transfers_info(filename):

    # get path basename
    base_name = os.path.basename(filename)
    
    FROM = base_name.split('_')[2]

    return FROM