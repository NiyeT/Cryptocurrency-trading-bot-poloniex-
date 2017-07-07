import poloniexAPI, re, threading
key=""
secret=""

coins={}
bestBuy=['',0]

class niye:
	def __init__(self):
		pass

	myCoins=['USDT_BTC']

	myCoinInfo={'USDT_BTC':{'amount':0.50}}


class coin:
	def __init__(self):
		pass

	name=''

	buyIn=0

	cashOut=0

poloniex=poloniexAPI.poloniexAPI(key,secret)

rawCoinData=poloniex.returnTicker()

btcExchangables=re.findall('BTC_[^\']+',str(rawCoinData))

for val in btcExchangables:
	if(rawCoinData[val]['isFrozen']=='1'):
		btcExchangables.remove(val)

#places coin information into a coin's object
def updateCoin(coinName):
	def x():
		current=coins[coinName]
		current.name=coinName
		current.buyIn=rawCoinData[coinName]['lowestAsk']
		current.cashOut=rawCoinData[coinName]['highestBid']	
		return current
	if(hasattr(coins,coinName)):
		return x()
	else:
		coins.update({coinName:coin()})
		return x()

#returns last buy ratio of a list of transactions
def calcBuyRatio(coin,transactions):
	previousExchange=''
	addType={'sell':0,'buy':0}
	start=''
	for transaction in transactions:
		exchangeType=transaction['type']
		if(previousExchange==''):
			if(start==''):
				start=exchangeType
			else:
				if(start!=exchangeType):
					previousExchange=exchangeType
		if(previousExchange!='' and previousExchange!=exchangeType):
			if(addType['buy']>0 and addType['sell']>0):
				return (addType['buy'] / (addType['buy'] + addType['sell'])) * 100
			previousExchange=exchangeType
			addType[exchangeType]=float(addType[exchangeType]) + float(transaction['amount'])
		elif(previousExchange==exchangeType):
			addType[exchangeType]=float(addType[exchangeType]) + float(transaction['amount'])

#checks if a coin is a better purchase than the coin currently considered to be the best
def highestBuyRatio(coinName):
	br=calcBuyRatio(coinName,poloniex.returnMarketTradeHistory(coinName))
	if(br>bestBuy[1]):
		bestBuy[0]=coinName
		bestBuy[1]=br
	elif(br==bestBuy[1]):
		if(coins[coinName].buyIn>coins[bestBuy[0]].buyIn):
			bestBuy[0]=coinName
			bestBuy[1]=br

def finalCheck(trans,coinName,ownership):
	def stillGood():
		calcBuyRatio(coinName,poloniex.returnMarketTradeHistory(coinName))
		if(calcBuyRatio>66.6):
			return poloniex.returnTicker()[coinName]['lowestAsk']
		else:
			return False

	def stillBad():
		calcBuyRatio(coinName,poloniex.returnMarketTradeHistory(coinName))
		if(calcBuyRatio<50):
			return poloniex.returunTicker()[coinName]['highestBid']
		else:
			return False

	def purchase():
		recentInfo=stillGood()
		if(recentInfo):
			rate=recentInfo
			amount=(niye.myCoinInfo['USDT_BTC']['amount'] / float(rawCoinData['USDT_BTC']['highestBid'])) / float(rate)
		poloniex.buy(coinName,rate,amount)
		print 'BOUGHT ' + coinName
		niye.myCoins.append(coinName)

	def sell():
		recentInfo=stillBad()
		if(recentInfo):
			fiftyCents=niye.myCoinInfo['USDT_BTC']['amount'] / float(rawCoinData['USDT_BTC']['highestBid'])
			amount=float(ownership[coinName]) / fiftyCents
			rate=recentInfo
			poloniex.sell(coinName,rate,amount)
			print 'SOLD ' + coinName
			if(amount==1):
				niye.myCoins.remove(coinName)


	if(trans=='buy'):
		purchase()
	if(trans=='sell'):
		sell()

def myReturns():
	finalCheck('buy',bestBuy[0],'')
	for val in niye.myCoins:
		finalCheck('sell',val,poloniex.returnBalances())
	

#just prints coin information for the sake of following along
def printCoin(coinName):
	current=coins[coinName]
	btcPrice=float(rawCoinData['USDT_BTC']['highestBid'])
	print current.name
	print 'BUY: $', float(current.buyIn) * btcPrice
	print 'SELL: $', float(current.cashOut) * btcPrice


#calls functions necessary for updating coin information for each coin
def updateAllCoins(coinList):
	for val in coinList:
		current=updateCoin(val)
		printCoin(val)
		highestBuyRatio(val)
		print 'BEST BUY:', bestBuy
		print '\n'
	myReturns()
	bestBuy[0]=''
	bestBuy[1]=0


def setInterval(time,func):
	def wrapper():
		def wrap():		
			func()
			cycle()
		wrap()
	def cycle():
		t=threading.Timer(time,wrapper)
		t.start()
	cycle()

def wrap():
	updateAllCoins(btcExchangables)

niye=niye()

setInterval(0.166666667,wrap)
