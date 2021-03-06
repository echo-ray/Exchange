from threading import Thread
from app.huobi.huobi import Huobi
from app.poloniex.poloniex import Poloniex
from function import *


class Comparer:
    def __init__(self, exchange1=Poloniex(), exchange2=Huobi(), currencypair=['BTC_USDT'], targe=['BTC_USDT']):
        logging.basicConfig(level=logging.INFO)
        self.exchange1 = exchange1
        self.exchange2 = exchange2
        self.exchange1.__init__(currencypair, targe)
        self.exchange2.__init__(currencypair, targe)
        self.exchange1.setTickerCompare(self.tickerCompare)
        self.exchange2.setTickerCompare(self.tickerCompare)
        self.exchange1.setTraderCompare(self.traderCompare)
        self.exchange2.setTraderCompare(self.traderCompare)
        self.t1 = Thread(target=self.exchange1.start)
        self.t2 = Thread(target=self.exchange2.start)
        self.noSupport = []

    def tickerPrinter(self, currencyPair):
        nowtime = timestampToDate(time.time() - time.timezone)
        print("{}'s Price : {} : {} , {} : {} time : {} ".format(currencyPair, self.exchange1, str(
            self.exchange1.ticker.data[currencyPair].price), self.exchange2,
                                                                 str(self.exchange2.ticker.data[
                                                                         currencyPair].price),
                                                                 nowtime))

    def tickerCompare(self, currencyPair):
        if currencyPair in self.noSupport:
            return
        elif not self.exchange1.ticker.isReady:
            logging.warning(MSG_TICKET_NOT_READY.format(self.exchange1))
        elif not self.exchange2.ticker.isReady:
            logging.warning(MSG_TICKET_NOT_READY.format(self.exchange2))
        else:
            try:
                self.tickerPrinter(currencyPair)
            except KeyError:
                if currencyPair not in self.exchange1.ticker.data:
                    logging.warning(MSG_NOT_SUPPORT_CURRENCY_PAIR.format(self.exchange1, currencyPair))
                else:
                    logging.warning(MSG_NOT_SUPPORT_CURRENCY_PAIR.format(self.exchange2, currencyPair))
                self.noSupport.append(currencyPair)

    def traderPrinter(self, currencyPair):
        askslow1 = min(list(map(float, self.exchange1.trader.data[currencyPair].asks.keys())))
        bidshigh1 = max(list(map(float, self.exchange1.trader.data[currencyPair].bids.keys())))
        askslow2 = min(list(map(float, self.exchange2.trader.data[currencyPair].asks.keys())))
        bidshigh2 = max(list(map(float, self.exchange2.trader.data[currencyPair].bids.keys())))
        nowtime = timestampToDate(time.time() - time.timezone)
        print("{}: {}'s Asks low : {}  Bids High : {} , {}'s Asks low : {}  Bids High : {} time : {} ".format(
            currencyPair, self.exchange1, askslow1, bidshigh1, self.exchange2, askslow2, bidshigh2, nowtime))

    def traderCompare(self, currencyPair):
        if currencyPair in self.noSupport:
            return
        try:
            if not self.exchange1.trader.isReady:
                logging.warning(MSG_TRADER_NOT_READY.format(self.exchange1))
            elif not self.exchange2.trader.isReady:
                logging.warning(MSG_TRADER_NOT_READY.format(self.exchange2))
            else:
                self.traderPrinter(currencyPair)
        except ValueError:
            if len(self.exchange1.trader.data[currencyPair].asks) == 0:
                logging.warning(
                    MSG_NOT_SUPPORT_CURRENCY_PAIR.format(self.exchange1, currencyPair))
            else:
                logging.warning(
                    MSG_NOT_SUPPORT_CURRENCY_PAIR.format(self.exchange2, currencyPair))
            # self.noSupport.append(currencyPair) # Init sequence bug

    def start(self):
        self.t1.start()
        self.t2.start()

    def close(self):
        self.exchange1.trader.restart = False
        self.exchange1.trader.ws.close()
        self.exchange1.ticker.restart = False
        self.exchange1.ticker.ws.close()
        self.exchange2.trader.restart = False
        self.exchange2.trader.ws.close()
        self.exchange2.ticker.restart = False
        self.exchange2.ticker.ws.close()
