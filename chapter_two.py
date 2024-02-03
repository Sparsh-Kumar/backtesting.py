'''
  - We are going to learn , how to implement strategy optimization.
  - It is basically an approach to get most suitable values of the variables we
   are going to use in the strategy for getting like maximum or minimum particular statistical value like sharpe ratio, minimum loss etc.
  - We implement optimization is by using `optimize()` method instead of `run()` on `Backtest()` instance.
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
stats = bt.optimize(
  upperBound=range(50, 85, 5),
  lowerBound=range(10, 45, 5),
  rsiWindow=range(10, 30, 2),
  maximize='Sharpe Ratio' # you can give here any statistical value that we get in the stats response.
)

print(stats)
bt.plot()
