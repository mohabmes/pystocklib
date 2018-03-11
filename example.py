from pystocklib import *

# Get the historical data
hist = HistoricalData('AAPL', from_date=[2005, 1, 1], to_date=[2018, 3, 1])
price = hist.get_high()
# or use: hist.retrieve_col_data('Open') 'Date', 'Open', 'High', 'Low', 'Adj', 'Close', 'Volume'

# # Plot & Generate CSV file
plot(price)
hist.create_csv()

# Load data from csv file
hist = HistoricalData()
hist.load_csv('AAPL')
hist.info_plot('Close')


# Apply EMD & show the figures
price = hist.get_close()
emd = EMD(price)
emd.save_figure('AAPL')
emd.save_figure('AAPL-trend', type='trend') # type => trend, all, modes, ds


# Calc The SD
sd = hist.standard_deviation('Open')
print(sd)

# get recent News
news = News('Apple')
result = news.get_result()
print(result)
