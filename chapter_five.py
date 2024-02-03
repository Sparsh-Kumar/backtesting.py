'''
  - In previous chapter, we learned how to optimize a custom metric.
  - In this chapter the main focus is to save the plot separately in a custom folder.
  - Let's say we need to add the plots in plot folder.
'''

import datetime
import pandas_ta as ta
import pandas as pd
import os

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
  constraint=lambda param: param.upperBound > param.lowerBound,
  # max_tries = 100 # This option is very useful for avoiding overfitting, from all combinations I would randomly select 100 combinations (not all) & then give result according to that.
)

# This piece of code is responsible for creating the folder & then saving the plot into that.
lowerBound = stats['_strategy'].lowerBound
upperBound = stats['_strategy'].upperBound
rsiWindow = stats['_strategy'].rsiWindow
if not os.path.exists('plots'):
  os.makedirs('plots')
fileName = f"plot-{lowerBound}-{upperBound}-{rsiWindow}.html"

print(stats)
bt.plot(filename=f"plots/{fileName}")

