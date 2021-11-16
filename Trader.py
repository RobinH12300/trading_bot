import MetaTrader5 as mt5


class Trader:
    deviation = 20

    def __init__(self, symbol):
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            print(symbol, "not found, can not call order_check()")
            mt5.shutdown()
            quit()

        # if the symbol is unavailable in MarketWatch, add it
        if not symbol_info.visible:
            print(symbol, "is not visible, trying to switch on")
            if not mt5.symbol_select(symbol, True):
                print("symbol_select({}}) failed, exit", symbol)
                mt5.shutdown()
                quit()

        self.symbol = symbol
        self.long_price = mt5.symbol_info_tick(symbol).ask
        self.short_price = mt5.symbol_info_tick(symbol).bid
        self.point = mt5.symbol_info(symbol).point

    def buildRequest(self, direction, lot, sl):

        if direction == "long":

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY,
                "price": self.long_price,
                "sl": self.long_price - sl * self.point,
                "deviation": self.deviation,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK,
            }

        else:

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_SELL,
                "price": self.short_price,
                "sl": self.short_price + sl * self.point,
                "deviation": self.deviation,
                "magic": 234000,
                "comment": "python script open",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK,
            }

        return request

    def checkOrder(self, direction, result, lot):
        # check the execution result
        if direction == "long":
            print(
                "Order_send()")
        else:
            print(
                "Order_send()")

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Order_send failed, retcode={}".format(result.retcode))
            # request the result as a dictionary and display it element by element
            result_dict = result._asdict()
            for field in result_dict.keys():
                print("   {}={}".format(field, result_dict[field]))
                # if this is a trading request structure, display it element by element as well
                if field == "request":
                    traderequest_dict = result_dict[field]._asdict()
                    for tradereq_filed in traderequest_dict:
                        print("       traderequest: {}={}".format(tradereq_filed, traderequest_dict[tradereq_filed]))
            print("shutdown() and quit")

        print("Order_send done, ", result)

    def sendOrder(self, direction, lot, sl):
        request = self.buildRequest(direction, lot, sl)
        result = mt5.order_send(request)

        self.checkOrder(direction, result, lot)

        return result

    def closeOrder(self, previous, lot, id):
        if previous == "buy":
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_SELL,
                "position": id,
                "price": self.short_price,
                "deviation": self.deviation,
                "magic": 234000,
                "comment": "python script close",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK,
            }

        else:
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": lot,
                "type": mt5.ORDER_TYPE_BUY,
                "position": id,
                "price": self.long_price,
                "deviation": self.deviation,
                "magic": 234000,
                "comment": "python script close",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK,
            }

        # send a trading request
        result = mt5.order_send(request)

        self.checkOrder(previous, result, lot)
        print("close position #")
