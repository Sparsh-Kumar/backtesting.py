'''
  - In previous chapter, we learned how to optimize a statistical measure.
  - We had optimized the parameters for maximum value of Sharpe Ratio.
  - Here we will see, how we can create our own statistical measure to optimize.
  - For example, we may want to maximize the ratio of `Equity Final [$]` / `Exposure Time [%]`.
  - So basically we want to find out the parameters which are responsible for maximum value of above given ratio.
  - The ratio basically represents the maximum amount of profit we can make by strategy being minimum time active in the market.
'''

import datetime
import pandas_ta as ta
import pandas as pd

from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG

# Return the metric from here, which we want to maximize.
def optim_func(series):
  # Now we want to make sure, that it optimizes this ratio but only show us those records
  # in which number of trades are greater than 10.
  # This piece of code would help us to do that.
  if series['# Trades'] < 10:
    return -1

  return series["Equity Final [$]"] / series["Exposure Time [%]"]

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
  upperBound=range(55, 85, 5),
  lowerBound=range(10, 45, 5),
  rsiWindow=range(10, 30, 2),
  maximize=optim_func, # Calling our custom function which would return the metric that we need to maximize.
  # We are ensuring to only look the combination in which upperBound values are greater than lowerBound values.
  # We can also make use of rsiWindow in it.
  constraint=lambda param: param.upperBound > param.lowerBound
)

print(stats)
bt.plot()

