'''
  - In this chapter we will learn how to invest only a fraction of our capital on each trade.
  - We can do this by using a parameter named "size" in buy().
  - Size would be a fraction like 0.1, It means you want to invest 10 % of your capital on each trade.
  - So, we can make use of Kelly Criterion as well.
'''

import os
import pandas_ta as ta
import pandas as pd

from backtesting import Backtest
from backtesting import Strategy  
from backtesting.lib import crossover
from backtesting.test import GOOG

class RsiOscillator(Strategy):

  upperBound = 70
  lowerBound = 30
  rsiWindow = 14

  def init(self):
    self.dailyRsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsiWindow)

  def next(self):

    if (crossover(self.dailyRsi, self.upperBound)):
      self.position.close()

    elif (crossover(self.lowerBound, self.dailyRsi)):
      # If you would give something like 1 or 2 here, then it would mean that
      # you have to buy these numbers of unit.
      # otherwise , if size = 0.1 , it means that we should invest 10% of capital on each trade.
      self.buy(size=0.1)

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


