'''
  - In this chapter we will learn how to use multitimeframe strategies in backtest.py.
  - By multitimeframe I mean for example you may have a strategy whose logic would be something like this
    - Buy/Sell when 20 Days rsi is below 30 & 20 hours rsi is also below 30 & 20 seconds rsi is below 40.
  - So backtesting.py allows you to calculate indicators in multi timeframe very easily.
  - Take a look at below example for reference.
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
    self.weeklyRsi = resample_apply(
      'W', ta.rsi, self.data.Close, self.rsiWindow
    )

  def next(self):
    if (crossover(self.weeklyRsi, self.upperBound)) and (crossover(self.dailyRsi, self.upperBound)):
      self.position.close()
    elif (crossover(self.lowerBound, self.dailyRsi)) and (crossover(self.lowerBound, self.weeklyRsi)):
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


