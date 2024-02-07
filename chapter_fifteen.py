
## In this chapter & chapter sixteen, we are going to learn how to use custom indicators
#### In this example, let's suppose that you have a sophisticated ML system that spits out signal column in the dataframe like -1, 0, 1
#### Where -1 means sell, 0 means remain neutral & 1 means buy.
#### Then we can directly feed those signals into backtesting.py
## Refer the example below


import numpy as np
from backtesting import Backtest, Strategy
from backtesting.test import GOOG

# Here we are randomly spitting out signals into Signal column
# As we are not using any sophisticated ML algos in the demonstration.
GOOG['Signal'] = np.random.randint(-1, 2, len(GOOG))

print(GOOG)


class SignalStrategy(Strategy):

  # init() function gets called once at the start when backtesting starts.
  def init(self):
    pass

  # next() gets called for every candle.
  def next(self):
    # The size of self.data.Close increases by 1 row, that means it iterates over the dataframe & insert the row in self.data for each iteration
    # We can access the current value of Close column using self.data.Close[-1], similarly we can access the previous value of Close column using self.data.Close[-2]
    print(f"Current Length of self.data is {len(self.data)} & the current value of closing price is {self.data.Close[-1]}")
    currentSignal = self.data.Signal[-1]
    if (currentSignal == 1):
      self.buy(size=0.1)
    elif (currentSignal == -1):
      # Please note we are not using self.sell() here, because it is for opening a short position, not actually closing the long position.
      # self.position.close() closes the current position that you have, if it is buy, then it will sell and vice-versa.
      self.position.close()


bt = Backtest(GOOG, SignalStrategy, cash=10000)
stats = bt.run()
print(stats)
bt.plot(filename=f"plots/random.html")
