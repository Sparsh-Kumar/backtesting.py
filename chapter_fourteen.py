'''
  - In this chapter we will learn how to use barsince function in backtesting.py
  The barssince function in backtesting.py is used to calculate the number of bars
  that have passed since a certain condition was met.
  - This can be useful for creating trading strategies that are based on specific market conditions.
  For example, you could use the barssince function to create a strategy that buys a stock
  when the RSI crosses above 70 and sells it when the RSI crosses below 30.
  You could also use the barssince function to create a strategy that only enters trades
  when the market has been trending in a certain direction for a certain number of bars.
'''

import os
import pandas_ta as ta
import pandas as pd

from backtesting import Backtest
from backtesting import Strategy  
from backtesting.lib import barssince
from backtesting.test import GOOG

class RsiOscillator(Strategy):

  upperBound = 70
  lowerBound = 30
  rsiWindow = 14

  def init(self):
    self.dailyRsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsiWindow)

  def next(self):

    # Here we are using barssince
    # Here the logic of barssince is
    # barssince(self.dailyRsi < self.upperBound) gives us the number of candles before which this condition was last seen.
    # and we are equating the above by 3, so technically we are saying that
    # Sell if (current rsi is above the upper bound value) && (there must be 3 candles before which the condition(rsi < upperbound)) is met.
    # So the rsi should be above upperbound for sometime.
    if (self.dailyRsi[-1] > self.upperBound) and (barssince(self.dailyRsi < self.upperBound) == 3):
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


