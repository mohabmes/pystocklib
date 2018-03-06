from pystocklib import *

# Get the historical data
hist = HistoricalData('AAPL')
price = hist.get_high() # or use: hist.retrieve_col_data('Open')

# Load data from csv file
hist = HistoricalData()
hist.load_csv('AAPL')
price = hist.get_close() # 'Date', 'Open', 'High', 'Low', 'Adj', 'Close', 'Volume'

# Plot & Generate CSV file
plot(price)
hist.create_csv('AAPL')

# Apply EMD & show the figures
emd = EMD(np.array(price))
emd.save_trend_figure('aapl_trend')
emd.plot_imf(type='all')

# Calc The SD
sdv = SDS(price)
value = sdv.get_standard_deviation()
print(value)

# get recent News
news = News('Apple')
result = news.get_result()
