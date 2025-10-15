# Using Python to query data from Subgraph API

It serves as a showcase of GraphQL utilization for blockchain data extraction.

It is designed to batch download Uniswap data for a given time period from multiple pools.

## Project Structure
1. Query pool creation data within a certain period:
    ```python
    subgraph_data('uniswap_v3', 'pools', block_begin, block_end)
    ```
2. Open saved JSON file to transform it into a csv file `pool_info.csv`.

3. Query swaps data
    
    3.1 Single pool:
    ```python
    subgraph_data('uniswap_v3','swaps', pool_address, block_begin, block_end)
    ```
   
    3.2 Batch Download
    ```python
    automate_query_data('uniswap_v3', 'pool_info.csv')
    ```
    

## Subgraph Endpoints
The project uses the following Uniswap subgraph endpoints:

- Uniswap V2: https://thegraph.com/explorer/subgraphs/A3Np3RQbaBA6oKJgiwDJeo5T3zrYfGHPWFYayMwtNDum
- Uniswap V3: https://thegraph.com/explorer/subgraphs/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV

## Obtaining a Subgraph API key
Querying data from Subgraphs requires an API key. You need to connect your wallet to Subgraph Studio and create API key. More information can be referred to Subgraph's docs [How to Manage API Key](https://thegraph.com/docs/en/subgraphs/querying/managing-api-keys/).


Include the API Key directly to the query endpoint. For example,

```python
url = "https://gateway.thegraph.com/api/{YOUR_API_KEY_HERE}/subgraphs/id/A3Np3RQbaBA6oKJgiwDJeo5T3zrYfGHPWFYayMwtNDum"
```
In this project, you need to create a `.env` file and paste your API key into it.

```python 
SUBGRAPH_API_KEY = "YOUR_API_KEY_HERE"
```

Users are offered 100,000 free queries every month to query Subgraphs.

## Quick Start

```python
import requests

url = "https://gateway.thegraph.com/api/{YOUR_API_KEY_HERE}/subgraphs/id/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV"

query = """
{swaps(first:5){

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
    id
    blockNumber
    timestamp
  }
  
  amount0
  amount1
  amountUSD
}
}
"""

response = requests.post(url, json={'query': query})
data = response.json()

print(data)

```


