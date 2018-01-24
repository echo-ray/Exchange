from .polonixeApi import PoloniexApi
from .socket.ticker import Ticker
from .socket.trader import Trader


class Poloniex:

    def __init__(self, currencypair=['BTC_USDT'], targe=['BTC_USDT']):
        self.ticker = Ticker(targe=targe)
        self.trader = Trader(currencypair=currencypair,targe=targe)
        self.caller = PoloniexApi()

    def __call__(self, currencypair, targe):
        self.ticker.targe = targe
        self.trader.currencypair = currencypair

    def start(self):
        self.ticker.start()
        self.trader.start()
    def __str__(self):
        return 'Poloniex'

    def setTickerCompare(self, function ):
        self.ticker.notice = function

    def setTraderCompare(self, function):
        self.trader.notice = function
