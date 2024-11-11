## INFO
I needed to multiple variables from my trades on the solana network that wasn't available from solscan or solana fm. This uses all public API's and doesn't require any private keys so should just be plug'n'play.

## Functions
1. Ask for transaction Signature
2. Retrieve timestamp and token amount from SolanaFM [transaction API](https://docs.solana.fm/reference/get_transfers)
3. Use [OHLC data](https://developers.binance.com/docs/binance-spot-api-docs/rest-api/public-rest-api-for-binance-2024-10-17) from BINCANCE public API to retrieve price of SOL/USDC since epoch time stamp.
4. Calculate the average buy price of the token
5. Displays the following:
    - Time of transaction
    - The price of SOL at the time of transaction
    - The amount of SOL used to buy the coin
    - The USD worth of SOL used to purchase the coin
    - The amount of tokens recieved
    - The total fees incurred during the transaction
    - The average buy price of the coin (see limitations)


## Limtitations
Since its using SOL/USDC the average buy price isn't exact to USD but its pretty close and won't affect overall gains and losses too considerably. Additionally, I can't retrieve CU limit or CU budget to calcualte the priority fees on the solanaFM api and cbf paying $199/month for solscan api. 

## Installation
1. Install dependencies
```shell
pip install -r requirements.txt
```
2. Run calc.py

---
@thomahn3 :)
