from .socket.ticker import Ticker
from .socket.trader import Trader
from threading import Thread
class Huobi:
    def __init__(self,currencypair=['BTC_USDT'],targe=['BTC_USDT']):
        self.ticker = Ticker(currencypair=currencypair,targe=targe)
        self.trader = Trader(currencypair=currencypair)
        self.name = 'Huobi'

    def start(self):
        self.ticker.start()
        self.trader.start()

    def setTickerCompare(self,function):
        self.ticker.notice = function

    def setTraderCompare(self,function):
        self.trader.notice =function