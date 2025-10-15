# (Uniswap V2) Subgraph URL: https://thegraph.com/hosted-service/subgraph/ianlapham/uniswapv2

# Call the public hosted TheGraph endpoint
# url = "https://api.thegraph.com/subgraphs/name/ianlapham/uniswapv2"

# ===========================Above is deprecated ===========================

# (Uniswap V2) Subgraph URL: https://thegraph.com/explorer/subgraphs/A3Np3RQbaBA6oKJgiwDJeo5T3zrYfGHPWFYayMwtNDum?view=Query&chain=arbitrum-one#query-subgraph

url = "https://gateway.thegraph.com/api/{api_key}/subgraphs/id/A3Np3RQbaBA6oKJgiwDJeo5T3zrYfGHPWFYayMwtNDum"

query = """
{
  swaps(first:1000, where:{
    pair : "%s", 
    transaction_:{
      blockNumber_gte:%i, 
      blockNumber_lt:%i},
    id_gt : "%s"
      }, 
      orderBy : id, 
      orderDirection : asc){

    id
	  transaction{
      blockNumber
    }
    timestamp
		sender
    from
    to
    amount0In
    amount1In
    amount0Out
    amount1Out
    amountUSD
    logIndex

    
  }
}
"""