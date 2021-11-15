import MetaTrader5 as mt5

class Depot:
    balance = 0
    position = 0

    def getPositionID(self):
        positions = mt5.positions_get(symbol="EURUSD")
        if positions == None:
            print("No positions on EURUSD, error code={}".format(mt5.last_error()))
        elif len(positions) > 0:
            print("Total positions on EURUSD =", len(positions))
            # display all open positions
            return positions[0][7]

    def changeBalance(self, amount):
        self.balance += amount

    def inceasePos(self):
        self.position += 1

    def decreasePos(self):
        self.position -= 1

    def __init__(self, amount):
        self.balance = amount