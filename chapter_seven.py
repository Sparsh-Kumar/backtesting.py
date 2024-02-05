'''
  - In previous chapter we saw how to create heatmaps.
  - But heatmap is basically a 2D figure, so how can we plot a third value ?.
  - We can create heatmap for all possible variables using plot_heatmaps().
  - The plot would get saved as a html file.
  - You can see from the example code below, that rsiWindow is a range, not a single number anymore.
'''

import pandas_ta as ta
import pandas as pd
import os
import matplotlib.pyplot as plt

from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover, plot_heatmaps
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
stats, heatmap = bt.optimize(
  upperBound=range(55, 85, 5),
  lowerBound=range(10, 45, 5),
  rsiWindow=range(10, 45, 5),
  maximize='Sharpe Ratio',
  # We are ensuring to only look the combination in which upperBound values are greater than lowerBound values.
  # We can also make use of rsiWindow in it.
  constraint=lambda param: param.upperBound > param.lowerBound,

  # This parameter would be responsible for returning heatmaps.
  return_heatmap=True
  # max_tries = 100 # This option is very useful for avoiding overfitting, from all combinations I would randomly select 100 combinations (not all) & then give result according to that.
)
if not os.path.exists('plots'):
  os.makedirs('plots')
fileName = f"plot.html"

# We can also see the plot getting saved in location plots.
plot_heatmaps(heatmap, agg='mean', filename=f"plots/{fileName}")

