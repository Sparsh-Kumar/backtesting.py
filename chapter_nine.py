'''
  - In this chapter we will learn how to implement shorting in the trading logic.
  - This can be done using self.sell() function.
  - self.position.close() is not a function for shorting, it is basically a function
  for closing all open positions.
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

  def init(self):
    self.dailyRsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsiWindow)

  def next(self):
    if (crossover(self.dailyRsi, self.upperBound)):
      if self.position.is_long:
        # We can also see various parameters in self.position like this
        print(self.position.size);
        print(self.position.pl_pct)
        self.position.close()
        self.sell()
    elif (crossover(self.lowerBound, self.dailyRsi)):
      if self.position.is_short or not self.position:
        self.position.close()
        self.buy()

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


