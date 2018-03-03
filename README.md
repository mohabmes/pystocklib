# pystocklib
Python package for Stock Market analysis. (Historical Data, EMD Trend signal, News extraction, News analysis, etc..)

# How to use

#### Get the historical data
```

hist = HistoricalData('AAPL')

# 'Date', 'Open', 'High', 'Low', 'Adj Close', 'Close', 'Volume'

price = hist.retrieve_col_data('close')

```

#### Plot & Generate CSV file
```

plot(price)

hist.create_csv('AAPL')

```

#### Apply EMD & show the figure
```

emd = EMD(np.asarray(price))

emd.plot_imf(type='all')

emd.save_trend_figure('aapl-trend')

```

#### Calc The SD
```

sdv = SDS(price)

value = sdv.get_standard_deviation()

print(value)

```

#### Gather News & analysis it
```

news = News('Apple')

result = news.get_result()

```
