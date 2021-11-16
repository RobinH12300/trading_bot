import datetime
import pandas as pd

import MetaTrader5 as mt5
import pytz

from Trader import Trader


class Ticker:
    time = ""
    timep = ""
    mma1 = 0
    mma2 = 0
    symbol = ""
    lot = 0

    def __init__(self, symbol, timeperiod, mma1, mma2, lot):
        self.timep = timeperiod
        self.symbol = symbol
        self.lot = lot

        if timeperiod == "1M":
            self.time = mt5.TIMEFRAME_M1
        elif timeperiod == "5M":
            self.time = mt5.TIMEFRAME_M5
        elif timeperiod == "10M":
            self.time = mt5.TIMEFRAME_M10
        elif timeperiod == "15M":
            self.time = mt5.TIMEFRAME_M15
        elif timeperiod == "1H":
            self.time = mt5.TIMEFRAME_H1
        elif timeperiod == "4H":
            self.time = mt5.TIMEFRAME_H4
        elif timeperiod == "1D":
            self.time = mt5.TIMEFRAME_D1

        self.mma1 = mma1
        self.mma2 = mma2

    def returnLot(self):
        return self.lot

    def InitTicks(self):
        rates = mt5.copy_rates_from_pos(self.symbol, self.time, 0, self.mma2)
        rates_frame = pd.DataFrame(rates)

        return rates_frame

    def getCurrentTick(self):
        self.timep = self.timep.replace("M", "")
        # TODO Wenn Std enthält oder Tag
        utc_from = datetime.datetime.now(pytz.timezone('Europe/Vienna')) - datetime.timedelta(hours=0,
                                                                                              minutes=int(self.timep))
        utc_to = datetime.datetime.now(pytz.timezone('Europe/Vienna'))

        rates = mt5.copy_rates_range(self.symbol, self.time, utc_from, utc_to)
        rates_frame = pd.DataFrame(rates)
        rates_frame[self.mma1] = 0
        rates_frame[self.mma2] = 0

        return rates_frame

    def calculateStartMMA(self, price):

        mma5 = []
        mma25 = []
        list5 = []
        list25 = []

        for i in range(self.mma2 - 1):
            mma5.append(0)
            mma25.append(0)

        for i in range(self.mma1):
            list5.append(price.iloc[-self.mma1 + i]["close"])

            if len(list5) >= self.mma1:
                avg5 = sum(list5) / self.mma1
                mma5.append(avg5)
                list5.pop(0)

        price[self.mma1] = mma5

        for i in range(self.mma2):
            list25.append(price.iloc[-self.mma2 + i]["close"])

            if len(list25) >= self.mma2:
                avg25 = sum(list25) / self.mma2
                mma25.append(avg25)
                list25.pop(0)

        price[self.mma2] = mma25

        return price

    def calculateTickMMA(self, price):
        list5 = []
        list25 = []
        counter = -1
        for i in range(len(price.tail(self.mma1))):
            list5.append(price.iloc[counter]["close"])
            counter -= 1

        counter = 1
        for i in range(len(price.tail(self.mma2))):
            list25.append(price.iloc[counter]["close"])
            counter -= 1

        avg5 = sum(list5) / self.mma1
        avg25 = sum(list25) / self.mma2

        price.at[self.mma2, self.mma1] = avg5
        price.at[self.mma2, self.mma2] = avg25

        return price

    def proofCross(self, trader, price, depot):
        listMMA5 = []
        listMMA25 = []
        global result

        for i in range(3):
            listMMA5.append(price.iloc[-3 + i][self.mma1])
            listMMA25.append(price.iloc[-3 + i][self.mma2])

        if listMMA5[0] < listMMA25[0] and listMMA5[1] < listMMA25[1] and listMMA5[2] > listMMA25[2]:
            if depot.position == 0:
                result = trader.sendOrder("long", self.lot, 150)
                depot.inceasePos()
            else:
                trader.closeOrder("short", self.lot, result.order)
                result = trader.sendOrder("long", self.lot, 150)
        elif listMMA5[0] > listMMA25[0] and listMMA5[1] > listMMA25[1] and listMMA5[2] < listMMA25[2]:
            if depot.position == 0:
                result = trader.sendOrder("short", self.lot, 150)
                depot.inceasePos()
            else:
                trader.closeOrder("long", self.lot, result.order)
                result = trader.sendOrder("short", self.lot, 150)
