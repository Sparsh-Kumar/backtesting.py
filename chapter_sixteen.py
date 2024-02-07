## In this chapter, we are going to implement the Bollinger Bands trading strategy.
## We would be making use of pandas_ta library

import numpy as np
import pandas_ta as ta
from backtesting import Backtest, Strategy
from backtesting.test import GOOG

print(GOOG)

def indicator(data):
  # data is going to be a OHLCV dataframe here,
  # But it does not necessarily to be like that, it can be any data with other column names different as well.
  # Important: See that we have used data.Close.s not data.Close, because when data is passed into indicator function
  ## pandas series gets converted into numpy array, but ta.bbands accepts a pandas series instead of pandas numpy array, so .s ensures that data.Close would get converted into pandas series while passing into ta.bbands
  bbands = ta.bbands(close=data.Close.s, std=1)
  return bbands.to_numpy().T[:3]

class BBStrategy(Strategy):

  def init(self):
    # As init function is called once.
    # We can calculate all the technical indicators here
    # We should not calculate the technical indicators in the next()
    # Because that function is called for every candle. So calculation would get executed for every candle, which is not required.
    # Anything that can be calculated at t = 0, needs to be here in this function.
    self.bbands = self.I(indicator, self.data)

  def next(self):
    lowerBand = self.bbands[0]
    upperBand = self.bbands[2]

    if self.data.Close[-1] > upperBand[-1]:
      self.position.close()
    elif self.data.Close[-1] < lowerBand[-1]:
      self.buy(size=0.1)


bt = Backtest(GOOG, BBStrategy, cash=10000)
stats = bt.run()
print(stats)
bt.plot(filename="plots/bb.html")
