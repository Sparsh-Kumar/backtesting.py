'''
 - Here we are using default data provided by backtesting.py framework (GOOG).
   We can also import our own data easily. But we have used the inbuilt data for learning purposes only.

 - In the code we are making use of `crossover` function provided by the backtesting.py framework,
   This function is mainly useful to implement crossover logic in trading strategies.

 - The `init` function gets called, when the strategy first starts executing, just like constructors.

 - The `next()` function gets called for every candle in the data.

 - The `Backtest()` is the method that is responsible for actual backtesting,
   It takes dataframe as first argument & then the strategy class.
'''

import datetime
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
    self.rsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsiWindow)

  def next(self):
    if crossover(self.rsi, self.upperBound):
      self.position.close()
    elif crossover(self.lowerBound, self.rsi):
      self.buy()
    
bt = Backtest(GOOG, RsiOscillator, cash=10000)
stats = bt.run()

print(stats)
