import time
import datetime

import MetaTrader5 as mt5
from Depot import Depot
from Ticker import Ticker
from Trader import Trader

# 41466651
# u65pAE55umE5
# AdmiralMarkets-Demo

username = 41466651
password = "u65pAE55umE5"
server = "AdmiralMarkets-Demo"
timeInSec = 900
tradinglist = ["[DAX40]"]
traderlist = []
tickerlist = []
pricelists = []


def logout():
    mt5.shutdown()


def init(username, pw, servername):
    # establish MetaTrader 5 connection to a specified trading account
    if not mt5.initialize(login=username, server=servername, password=pw):
        print("initialize() failed, error code =", mt5.last_error())
        quit()
    else:
        print("Login successful")


def trade(tickerlist, traderlist, pricelists):
    print("start trading")

    while True:
        while datetime.datetime.now().minute not in {0, 15, 30, 45}:  # Wait 1 second until we are synced up with the 'every 15 minutes' clock
            time.sleep(1)

        for i in range(len(pricelists)):
            pricelists[i] = pricelists[i].append(tickerlist[i].getCurrentTick(), ignore_index=True)

        time.sleep(2)

        for i in range(len(pricelists)):
            pricelists[i] = tickerlist[i].calculateTickMMA(pricelists[i])

        time.sleep(2)
        #priceDAX = priceDAX.append(ticker.getCurrentTick(), ignore_index=True)
        #time.sleep(2)
        #priceDAX = ticker.calculateTickMMA(priceDAX)

        #  priceDow = priceDow.append(tickerDow.getCurrentTick(), ignore_index=True)
        #time.sleep(2)
        #  priceDow = tickerDow.calculateTickMMA(priceDow)

        #   priceEUR = priceEUR.append(tickerEUR.getCurrentTick(), ignore_index=True)
        #time.sleep(2)
        #   priceEUR = tickerEUR.calculateTickMMA(priceEUR)

        for i in range(len(pricelists)):
            print(pricelists[i].tail(3))
        # print(priceDow.tail(3))
        # print(priceEUR.tail(3))

        """Fehlerprüfung"""
        for i in range(len(pricelists)):
            if len(pricelists[i]) >= 27:
                pricelists[i].drop(index=pricelists[i].index[0], axis=0, inplace=True)
                pricelists[i] = tickerlist[i].calculateTickMMA(pricelists[i])
                print("gekürzt")

        for i in range(len(pricelists)):
            tickerlist[i].proofCross(traderlist[i], pricelists[i], depot)
            pricelists[i].drop(index=pricelists[i].index[0], axis=0, inplace=True)

        # tickerDow.proofCross(traderDow, priceDow, depot)
        # tickerEUR.proofCross(traderEUR, priceEUR, depot)


        #  priceDAX = priceDAX.iloc[1:]
        # priceDow = priceDow.iloc[1:]
        # priceEUR = priceEUR.iloc[1:]
        time.sleep(4)


def starting():
    print("starting Bot...")
    init(username, password, server)

    for element in tradinglist:
        tickerlist.append(Ticker(element, "15M", 5, 25, 1.0))
        traderlist.append(Trader(element))

    for i in range(len(tradinglist)):
        pricelists.append(tickerlist[i].InitTicks())

    for i in range(len(pricelists)):
        pricelists[i] = tickerlist[i].calculateStartMMA(pricelists[i])

    trade(tickerlist, traderlist, pricelists)
    #ticker = Ticker("[DAX40]", "15M", 5, 25)
    #trader = Trader("[DAX40]")
    #priceDAX = ticker.InitTicks()
    #priceDAX = ticker.calculateStartMMA(priceDAX)

    # tickerDow = Ticker("[DJI30]", "15M", 5, 25)
    # traderDow = Trader("[DJI30]")
    # priceDow = ticker.InitTicks()
    # priceDow = ticker.calculateStartMMA(priceDow)

    # tickerEUR = Ticker("EURUSD", "15M", 5, 25)
    # traderEUR = Trader("EURUSD")
    # priceEUR = tickerEUR.InitTicks()
    # priceEUR = tickerEUR.calculateStartMMA(priceEUR)

def shutdown():
    print("shutdown Bot...")
    if len(mt5.positions_get()) > 0:
        for i in range(len(tradinglist)):
            position = mt5.positions_get(group=traderlist[i])
            if position == None:
                mt5.shutdown()
            else:
                position_id = depot.getPositionID(position)
                position_direction = depot.getPositionDirection(position)

                if position_direction == 0:
                    traderlist[i].closeOrder("buy", tickerlist[i].returnLot(), position_id)
                else:
                    traderlist[i].closeOrder("buy", tickerlist[i].returnLot(), position_id)

depot = Depot(mt5.symbols_get())
while datetime.datetime.now().minute not in {0, 15, 30, 45}:  # Wait 1 second until we are synced up with the 'every 15 minutes' clock
        time.sleep(1)
starting()
