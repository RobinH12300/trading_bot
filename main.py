import datetime
import time

import MetaTrader5 as mt5

# 41466651
# u65pAE55umE5
# AdmiralMarkets-Demo
import pytz

from Depot import Depot
from Ticker import Ticker
from Trader import Trader

username = 41466651
password = "u65pAE55umE5"
server = "AdmiralMarkets-Demo"
timeInSec = 900


def logout():
    mt5.shutdown()


def init(username, pw, servername):
    # establish MetaTrader 5 connection to a specified trading account
    if not mt5.initialize(login=username, server=servername, password=pw):
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    else:
        print("Login successful")


init(username, password, server)
depot = Depot(10000)

ticker = Ticker("[DAX40]", "15M", 5, 25)
trader = Trader("[DAX40]")
priceDAX = ticker.InitTicks()
priceDAX = ticker.calculateStartMMA(priceDAX)

#tickerDow = Ticker("[DJI30]", "15M", 5, 25)
#traderDow = Trader("[DJI30]")
#priceDow = ticker.InitTicks()
#priceDow = ticker.calculateStartMMA(priceDow)

#tickerEUR = Ticker("EURUSD", "15M", 5, 25)
#traderEUR = Trader("EURUSD")
#priceEUR = tickerEUR.InitTicks()
#priceEUR = tickerEUR.calculateStartMMA(priceEUR)


print("Wait until Start")
# warte bis nächste volle 5 Min
t = datetime.datetime.now(pytz.timezone('Europe/Vienna'))
sleeptime = 60 - (t.second + t.microsecond / 1000000.0)
time.sleep(sleeptime)

print("Start Trading")

while True:
    time.sleep(timeInSec-8)

    priceDAX = priceDAX.append(ticker.getCurrentTick(), ignore_index=True)
    time.sleep(2)
    priceDAX = ticker.calculateTickMMA(priceDAX)

  #  priceDow = priceDow.append(tickerDow.getCurrentTick(), ignore_index=True)
    time.sleep(2)
  #  priceDow = tickerDow.calculateTickMMA(priceDow)

 #   priceEUR = priceEUR.append(tickerEUR.getCurrentTick(), ignore_index=True)
    time.sleep(2)
 #   priceEUR = tickerEUR.calculateTickMMA(priceEUR)

    print(priceDAX.tail(3))
    #print(priceDow.tail(3))
   # print(priceEUR.tail(3))

    ticker.proofCross(trader, priceDAX, depot)
   # tickerDow.proofCross(traderDow, priceDow, depot)
   # tickerEUR.proofCross(traderEUR, priceEUR, depot)

    priceDAX.drop(index=priceDAX.index[0], axis=0, inplace=True)
  #  priceDAX = priceDAX.iloc[1:]
   # priceDow = priceDow.iloc[1:]
   # priceEUR = priceEUR.iloc[1:]
    time.sleep(4)

