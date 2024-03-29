'''
  - In this chapter, we will see how to plot heatmaps.
  - We would be making use of seaborn along with matplotlib.
'''

import pandas_ta as ta
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
stats, heatmap = bt.optimize(
  upperBound=range(55, 85, 5),
  lowerBound=range(10, 45, 5),
  rsiWindow=14,
  maximize='Sharpe Ratio',
  # We are ensuring to only look the combination in which upperBound values are greater than lowerBound values.
  # We can also make use of rsiWindow in it.
  constraint=lambda param: param.upperBound > param.lowerBound,

  # This parameter would be responsible for returning heatmaps.
  return_heatmap=True
  # max_tries = 100 # This option is very useful for avoiding overfitting, from all combinations I would randomly select 100 combinations (not all) & then give result according to that.
)

print(heatmap)

# Plotting heatmap
hm = heatmap.groupby(['upperBound', 'lowerBound']).mean().unstack()

# cmap is an optional argument which is basically a color theme for heat map.
sns.heatmap(hm, cmap='viridis')
plt.show()


