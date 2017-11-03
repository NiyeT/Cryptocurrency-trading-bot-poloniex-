# Cryptocurrency Trading Bot (Poloniex)

Simple cryptocurrency exchange bot built for testing purposes on the poloniex API

# Installation

• Clone the repository

````sh
git clone https://github.com/NiyeT/Cryptocurrency-trading-bot-poloniex-.git
````

• cd into cryptocurrency_trading_bot

````sh
cd cryptocurrency_trading_bot
````

• Change the key and secret in PoloniexAPI.py to match your own credentials.
  -Instructions on getting your key and secret can be found here:
  https://coinigy.freshdesk.com/support/solutions/articles/1000087491-how-do-i-find-my-api-key-on-poloniex-com-
  
![alt text](https://i.imgur.com/e4BVp1G.png)

# Usage (methods)

• updateCoin
  -takes: 
    coin ticker
  -returns: 
    void > strips coin name, buyIn, and cashOut values and places them into the coin object
 
````python
updateCoin("BTC")
````

• calcBuyRatio
  -takes:
    coin name
    transaction list
  -returns:
    float representing "most recent" buy to sell ratio

````python
coin="BTC"
transactions=[{ "globalTradeID": 25129732, "tradeID": "6325758", "date": "2016-04-05 08:08:40", "rate": "0.02565498", "amount": "0.10000000", "total": "0.00256549", "fee": "0.00200000", "orderNumber": "34225313575", "type": "sell", "category": "exchange" }, { "globalTradeID": 25129628, "tradeID": "6325741", "date": "2016-04-05 08:07:55", "rate": "0.02565499", "amount": "0.10000000", "total": "0.00256549", "fee": "0.00200000", "orderNumber": "34225195693", "type": "buy", "category": "exchange" }]

calcBuyRatio(coin,transactions)
````

