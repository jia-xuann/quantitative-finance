# load the library
import requests
import json
import pandas as pd
# import logging
import os
from dotenv import load_dotenv

# load environment variables
_ = load_dotenv()
api_key = os.getenv("SUBGRAPH_API_KEY")

# locate the folder
script_dir = os.path.dirname(os.path.abspath(__file__))
# change the working directory
os.chdir(script_dir)

# ==================================Environment Setting==================================


# set the time frame
# we want to collect the 2-year pool info during 2021-01-01 and 2022-12-31, 
# additionally, to make a half-year observation window for each launch project, 
# we extend the period to 2023-06-30 

BlockBegin = 11565019
# block_begin = 11565019 # Jan-01-2021 12:00:00 AM +UTC
BlockEnd = 17595510 # Jul-01-2023 12:00:11 AM +UTC
# gap = 500


def subgraph_data(platform, activity,  pool_address=None, block_begin=BlockBegin, block_end = BlockEnd):
    # ==========================Query the data from The Graph==================================
    # ===================Query pool creation data ===================
    if activity == 'pools':

            if platform == 'uniswap_v2':
                from query_pool_uniswap_v2 import query, url
                activity = 'pairs'

            if platform == 'uniswap_v3':
                # load the query for dumping pool creation data
                from query_pool_uniswap_v3 import query, url

            url_var = url.format(api_key=api_key)
            
            # initialize the setting
            last_id = ""
            data_overload = True

            # loop the request for query limit 
            all_pools = []

            while data_overload:
                
                query_var = query%(block_begin, block_end, last_id)
                response = requests.post(url_var, json={'query':query_var})
                
    
                # Transform the string into a json object
                json_data = response.json()
                                  
                # Check data availability
                # if subgraph lacks of the related data, then it return the query as "error" even though the status is correct
                if 'data' in json_data and activity in json_data['data']:

                    pools = json_data['data'][activity]
                    if pools == []:
                        data_overload = False
                        print("Block %i-%i: None"%(block_begin, block_end))
                        

                    else:
                    
                        # Determine if there are more data to fetch
                        data_overload = len(pools) == 100
                        if data_overload:
                            # Set the cursor to the id of the last dumped pool creation
                            last_id = pools[-1]['id']

                        # add up pools
                        all_pools.extend(pools)

                        print("Dumped Data Count: ", len(all_pools))

    # ===================Query swap data ===================
    if activity == 'swaps':
        if pool_address is None:
            raise ValueError("Please provide a pool address for querying swap data.")
        else:
            if platform == 'uniswap_v2':
                from query_swap_uniswap_v2 import query, url
            
            if platform == 'uniswap_v3':
                from query_swap_uniswap_v3 import query, url

            url_var = url.format(api_key=api_key)
            # initialize the setting
            last_id = ""
            data_overload = True

            # loop the request for query limit 
            all_swaps = []

            while data_overload:
                
                query_var = query%(pool_address, block_begin, block_end, last_id)
                # logging.debug(query%(pool_address, tmp_0, tmp_1))
                response = requests.post(url_var, json={'query':query_var})
                
    
                
                # The request returns a json structured string. Therefore, we transform the string into a json object
                json_data = response.json()
                                  
                

                # if subgraph lacks of the related data, then it return the query as "error" even though the status is correct
                if 'data' in json_data and activity in json_data['data']:
                

                    swaps = json_data['data'][activity]
                    if swaps == []:
                        data_overload = False
                        print("Block %i-%i: None"%(block_begin, block_end))
                        

                    else:
                    
                        # Determine if there are more data to fetch
                        data_overload = len(swaps) == 1000
                        if data_overload:
                            # Set the cursor to the id of the last dumped transation 
                            last_id = swaps[-1]['id']

                        # add up swaps
                        all_swaps.extend(swaps)
        
                        print("Dumped Data Count: ", len(all_swaps))
                                                       
    # ==========================Store the data==================================
    # check if the data storage folder exists
    # create a folder and ignore if it already exists
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Created folder: data")

    if activity == 'pools' or activity == 'pairs':

        # Store the JSON data in a file
        save_name = os.path.join('data', 'pool_info.' + platform + '.json')

        with open(save_name, "w") as file:
            json.dump({'pairs' : all_pools}, file)

    if activity == 'swaps':
        storage_path = os.path.join('data', platform)
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)
            print("Created folder: %s"%storage_path)

        # Store the JSON data in a file
        save_name = os.path.join(storage_path, pool_address + '.json')
    

        with open(save_name, "w") as file:
            json.dump({'swaps' : all_swaps}, file)


    print("Data stored successfully!")

# ======================Massive download swap data from a list of pools=========================
def automate_query_data(platform, csvfile_name):
    
    # Read the CSV file to get the pool addresses and block numbers
    file = pd.read_csv(csvfile_name)

    # filter out the fields with matched platform
    df = file[file['platform'] == platform] 
    
    # report the summary
    length = len(df)
    print("There are %i rows in total"%length)

    for row in df.index:

        pool_address = df.loc[row, 'id']
        block_begin = df.loc[row, 'createdAtBlockNumber']

        save_path = os.path.join('data', platform, pool_address + '.json')

         # check if the save_name file already exists
        if os.path.exists(save_path):
            print('platform:', platform)
            print("Skipping pool %s. Already downloaded."%(pool_address))
        
        else:
            subgraph_data(platform, 'swaps', pool_address, block_begin=block_begin)
            print('platform:', platform)
            print("from pool: %s"%pool_address)

        length -= 1
        print("Remaining %i items in queue\n"%length)


if (__name__) == '__main__':
     
    # activity = ['pools', 'swaps']
    
# ===================Example 1: Query pool creation data ===================
    subgraph_data('uniswap_v2', 'pools', block_begin=BlockBegin, block_end=BlockBegin+10000)
    # subgraph_data('uniswap_v3', 'pools', block_begin=BlockBegin, block_end=BlockEnd) 

# ===================Example 2: Query swap data from a specific pool ===================
    pool_address = '0xcbcdf9626bc03e24f779434178a73a0b4bad62ed' # Uniswap V3 WBTC/WETH pool
    block_begin = 12369879
    block_end = block_begin + 500
    subgraph_data('uniswap_v3','swaps', pool_address=pool_address, block_begin=block_begin, block_end=block_end)



# ===================Example 3: Automate query data from a list of pools ===================
# Careful: The Graph API begins to charge fees. It provides some free quota.
# The Free Plan includes 100,000 free monthly queries

    automate_query_data('uniswap_v2', 'pool_info.csv')


