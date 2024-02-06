'''
  - In this chapter we will learn how to implement take profit & stop loss
    in the existing strategy.
  - Important -> Sometimes, when the stop loss hits, then in the next candle a buy position is opened.
    This can be very dangerous and we should avoid these kind of scenarios in the trading strategy.
  - Important -> Also avoid immediate buy after selling condition, like selling now & buying in next candle.
    This type of situation also needs to be taken care of in real life scenarios.
'''

import os
import pandas_ta as ta
import pandas as pd

from backtesting import Backtest
from backtesting import Strategy  
from backtesting.lib import crossover, resample_apply
from backtesting.test import GOOG

class RsiOscillator(Strategy):

  upperBound = 70
  lowerBound = 30
  rsiWindow = 14
  sl = 5/100;
  tp = 15/100

  def init(self):
    self.dailyRsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsiWindow)

  def next(self):

    slPrice = ((1 - self.sl) * self.data.Close[-1])
    tpPrice = ((1 + self.tp) * self.data.Close[-1])

    if (crossover(self.dailyRsi, self.upperBound)):
      self.position.close()

    # So when price drops to 0.95 times of current closing price.
    # Or we can say when the price drops by 5%. That price value would be our stop loss.
    # self.data.Close[-1] is used to take the latest value of closing price.
    elif (crossover(self.lowerBound, self.dailyRsi)):
      self.buy(tp=tpPrice, sl=slPrice)

bt = Backtest(GOOG, RsiOscillator, cash=10000)

stats = bt.run()
print(stats)

lowerBound = stats['_strategy'].lowerBound
upperBound = stats['_strategy'].upperBound
rsiWindow = stats['_strategy'].rsiWindow

if not os.path.exists('plots'):
  os.makedirs('plots')

fileName = f"plot-{lowerBound}-{upperBound}-{rsiWindow}.html"
bt.plot(filename=f"plots/{fileName}")


