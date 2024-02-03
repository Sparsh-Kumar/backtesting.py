'''
  - We are going to learn , how to implement constraints while strategy optimization.
  - As you can see from the code, we are trying to optimize the parameters for our RsiOscillator strategy.
  - But as you can see, the upperBound values & lowerBound values are same. But it does not make sense, because we
   want that upperBound value should be greater than lowerBound values for all combinations of upperBound & lowerBound.

   Disadvantages of Over Parameter Optimization
   --------------------------------------------
   - Overfitting: One of the main challenges in parameter optimization is the risk of overfitting.
     When you optimize your strategy parameters based on historical data, there's a possibility that your strategy becomes too specific to the historical dataset and may not perform well on new, unseen data.
   - Data Snooping Bias: If you iterate over different combinations of parameters multiple times using the same dataset, you might unintentionally find a set of parameters that work well purely due to chance.
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
  upperBound=range(10, 45, 5),
  lowerBound=range(10, 45, 5),
  rsiWindow=range(10, 30, 2),
  maximize='Sharpe Ratio',
  # We are ensuring to only look the combination in which upperBound values are greater than lowerBound values.
  # We can also make use of rsiWindow in it.
  constraint=lambda param: param.upperBound > param.lowerBound
)

print(stats)
bt.plot()

