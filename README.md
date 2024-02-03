# Overview

## What is Backtesting ?.

Backtesting is a process used in finance to assess the effectiveness of a trading strategy. It involves testing a strategy using historical market data to see how it would have performed in the past.

## About `Backtesting.py`

`Backtesting.py` is a Python library that simplifies the process of backtesting trading strategies. It provides tools and metrics to evaluate the performance of your strategies using historical data.

## Usage

To get started with backtesting.py, you can follow these steps:

1. Install the required dependencies.
2. Clone this repository:
3. `git clone https://github.com/Sparsh-Kumar/backtesting.py.git`
4. `cd backtesting.py`
5. Each chapter in this repository is suffixed by `_{{chapter_number}}`.

# Understanding Backtesting Stats

After running a backtest, you will receive a set of statistics. Here's a breakdown of the meaning of each stat:

1. **Start**: The start date of the backtesting period.
2. **End**: The end date of the backtesting period.
3. **Duration**: The total duration of the backtesting period.
4. **Exposure Time [%]**: The percentage of time your strategy was invested.
5. **Equity Final [$]**: The final equity value after the backtesting period.
6. **Equity Peak [$]**: The highest equity value during the backtesting period.
7. **Return [%]**: The overall return percentage of your strategy.
8. **Buy & Hold Return [%]**: The return percentage if you had bought and held the asset throughout the entire period.
9. **Return (Ann.) [%]**: Annualized return percentage.
10. **Volatility (Ann.) [%]**: Annualized volatility, a measure of the asset's price variability.
11. **Sharpe Ratio**: A risk-adjusted measure of performance. It indicates the excess return per unit of risk. [More Info](https://www.investopedia.com/terms/s/sharperatio.asp).
12. **Sortino Ratio**: Similar to the Sharpe Ratio but focuses only on downside risk. [More Info](https://www.investopedia.com/terms/s/sortinoratio.asp)
13. **Calmar Ratio**: The ratio of the annualized return to the maximum drawdown. It measures the relationship between return and drawdown. [More Info](https://www.investopedia.com/terms/c/calmarratio.asp)
14. **Max. Drawdown [%]**: The maximum percentage drop in equity from a peak to a trough. [More Info](https://www.investopedia.com/terms/m/maximum-drawdown-mdd.asp)
15. **Avg. Drawdown [%]**: The average percentage drop during drawdown periods.
16. **Max. Drawdown Duration**: The duration of the longest drawdown period.
17. **Avg. Drawdown Duration**: The average duration of drawdown periods.
18. **Trades**: The total number of trades executed.
19. **Win Rate [%]**: The percentage of trades that were profitable.
20. **Best Trade [%]**: The highest percentage return from a single trade.
21. **Worst Trade [%]**: The lowest percentage return from a single trade.
22. **Avg. Trade [%]**: The average percentage return per trade.
23. **Max. Trade Duration**: The duration of the longest single trade.
24. **Avg. Trade Duration**: The average duration of all trades.
25. **Profit Factor**: The ratio of gross profits to gross losses.
26. **Expectancy [%]**: The average expected return per trade.
27. **SQN (System Quality Number)**: A measure of the quality of a trading system based on its expectancy and the statistical significance of the outcome. [More Info](https://medium.com/@niclas_hummel/system-quality-number-sqn-cb04cf7e9ecd)

## Contributing

Contributions are welcome! Feel free to open issues or pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Sparsh-Kumar/backtesting.py/blob/main/LICENSE) file for details

