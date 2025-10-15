# (Uniswap V3) Subgraph URL: https://thegraph.com/explorer/subgraph/uniswap/uniswap-v3

# Call the public hosted TheGraph endpoint 
# url = 'https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3'
# ===========================Above is deprecated ===========================

# (Uniswap V3) Subgraph URL: https://thegraph.com/explorer/subgraphs/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV?view=Query&chain=arbitrum-one#query-subgraph

url = 'https://gateway.thegraph.com/api/{api_key}/subgraphs/id/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV'


query = """
{
  swaps(first : 1000, where:{
    pool:"%s", 
    transaction_:{
      blockNumber_gte:%i, 
      blockNumber_lt:%i},
    id_gt: "%s"
    }, 

    orderBy:id, 
    orderDirection:asc){

    id
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
    logIndex
    

    
  }
}
"""