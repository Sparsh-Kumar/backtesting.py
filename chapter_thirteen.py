'''
  - In this chapter we will learn how to get a dataframe which has all the information
  regarding all the trades that are been done in the backtesting.
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

    elif self.dailyRsi[-1] < self.lowerBound:
      # If you would give something like 1 or 2 here, then it would mean that
      # you have to buy these numbers of unit.
      # otherwise , if size = 0.1 , it means that we should invest 10% of capital on each trade.
      self.buy(size=1)

bt = Backtest(GOOG, RsiOscillator, cash=10000)

stats = bt.run()

# This line would print all the trades in a very formatted dataframe.
# You can create reports , feed the information to another algo etc.
# We have converted it into a big string, because it was large in size & thus was
# not visible as pandas dataframe
print(stats['_trades'].to_string())

lowerBound = stats['_strategy'].lowerBound
upperBound = stats['_strategy'].upperBound
rsiWindow = stats['_strategy'].rsiWindow

if not os.path.exists('plots'):
  os.makedirs('plots')

fileName = f"plot-{lowerBound}-{upperBound}-{rsiWindow}.html"
bt.plot(filename=f"plots/{fileName}")


