# load the library
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
_ = load_dotenv()
api_key = os.getenv("SUBGRAPH_API_KEY")

if not api_key:
    raise ValueError("API key not found. Please set the SUBGRAPH_API_KEY environment variable.")


# ===================Test 1: Query swap data ===================
from query_swap_uniswap_v3 import url
url_var_swap = url.format(api_key=api_key)

query_swap = """
{swaps(first:5, orderBy:timestamp, 
  where:{
  transaction_:{
    blockNumber_gte:11565019
  }
})
{
    pool{
    id
    token0{
      symbol
    }
    token1{
      symbol
    }
  }
	  transaction{
      blockNumber
    }
    timestamp
		sender
    recipient
    origin
    amount0
    amount1
    amountUSD
  	id
    logIndex
  
}
}
"""
response = requests.post(url_var_swap, json={'query':query_swap})

if response.status_code != 200:
    raise Exception(f"Query failed with status code {response.status_code}: {response.text}")   
json_data = response.json()
df = pd.json_normalize(json_data['data']['swaps'])
print(df)


# ===================Test 2: Query pool creation data ===================
from query_pool_uniswap_v2 import url
url_var_pool = url.format(api_key=api_key)

query_pool = """
{{
  pairs(first:10){
    id
    token0{
      id
      symbol
      decimals
      
    }
    token1{
      id
      symbol
      decimals
      
    }
    createdAtBlockNumber
    createdAtTimestamp
  }
}
"""
response = requests.post(url_var_pool, json={'query':query_pool})
response = requests.post(url_var_swap, json={'query':query_swap})

if response.status_code != 200:
    raise Exception(f"Query failed with status code {response.status_code}: {response.text}")   
json_data = response.json()
df = pd.json_normalize(json_data['data']['pairs'])
print(df)