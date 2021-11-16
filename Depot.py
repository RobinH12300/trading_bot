import MetaTrader5 as mt5

class Depot:
    balance = 0
    position = 0

    def getPositionID(self, pos):
        return pos[0][7]

    def getPositionDirection(self, pos):
        return pos[0][2]

    def changeBalance(self, amount):
        self.balance += amount

    def inceasePos(self):
        self.position += 1

    def decreasePos(self):
        self.position -= 1

    def __init__(self, amount):
        self.balance = amount