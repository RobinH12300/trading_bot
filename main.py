import time
import datetime

import MetaTrader5 as mt5
from Depot import Depot
from Ticker import Ticker
from Trader import Trader
import pandas as pd

# 41466651
# u65pAE55umE5
# AdmiralMarkets-Demo

username = 41466651
password = "u65pAE55umE5"
server = "AdmiralMarkets-Demo"
Minutes = 5
timeInSec = 60 * Minutes
tradinglist = ["[DJI30]"]
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
    delay = 0
    while True:
        print("Delay: " + str(timeInSec - delay))
        time.sleep(timeInSec - delay)
        delay = datetime.datetime.now().second

        for i in range(len(pricelists)):
            pricelists[i] = pricelists[i].append(tickerlist[i].getCurrentTick(), ignore_index=True)

        for i in range(len(pricelists)):
            pricelists[i] = tickerlist[i].calculateTickMMA(pricelists[i])

        for i in range(len(pricelists)):
            print(pricelists[i].tail(3))

        """Fehlerprüfung"""
        for i in range(len(pricelists)):
            if len(pricelists[i]) >= 27:
                pricelists[i].drop(index=pricelists[i].index[0], axis=0, inplace=True)
                pricelists[i] = tickerlist[i].calculateTickMMA(pricelists[i])
                print("gekürzt:")

                # create DataFrame out of the obtained data
                rates_frame = pd.DataFrame(pricelists[i])
                # convert time in seconds into the 'datetime' format
                rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
                print(rates_frame)

        for i in range(len(pricelists)):
            tickerlist[i].proofCross(traderlist[i], pricelists[i], depot)
            pricelists[i].drop(index=pricelists[i].index[0], axis=0, inplace=True)


def starting():
    print("starting Bot...")
    init(username, password, server)

    for element in tradinglist:
        tickerlist.append(Ticker(element, "5M", 5, 25, 1.0))
        traderlist.append(Trader(element))

    for i in range(len(tradinglist)):
        pricelists.append(tickerlist[i].InitTicks())

    for i in range(len(pricelists)):
        pricelists[i] = tickerlist[i].calculateStartMMA(pricelists[i])

    trade(tickerlist, traderlist, pricelists)


def shutdown():
    print("shutdown Bot...")
    if len(mt5.positions_get()) > 0:
        for i in range(len(tradinglist)):
            position = mt5.positions_get(group=traderlist[i])
            if position is None:
                mt5.shutdown()
            else:
                position_id = depot.getPositionID(position)
                position_direction = depot.getPositionDirection(position)

                if position_direction == 0:
                    traderlist[i].closeOrder("buy", tickerlist[i].returnLot(), position_id)
                else:
                    traderlist[i].closeOrder("sell", tickerlist[i].returnLot(), position_id)


depot = Depot(mt5.symbols_get())
c = 0
if c == 0:
    while datetime.datetime.now().minute not in {0, 55, 30, 45}:
        # Wait 1 second until we are synced up with the 'every 15 minutes' clock
        time.sleep(1)
print("START")
c += 1
if c == 1:
    starting()
