from pystocklib import *

# Get the historical data
hist = HistoricalData('GOOG', from_date=[2005, 1, 1], to_date=[2018, 3, 1])
price = hist.get_high() # or use: hist.retrieve_col_data('Open')

# # Plot & Generate CSV file
plot(price)
hist.create_csv('GOOG')

# Load data from csv file
hist = HistoricalData()
hist.load_csv('GOOG')
price = hist.get_close() # 'Date', 'Open', 'High', 'Low', 'Adj', 'Close', 'Volume'

# Apply EMD & show the figures
emd = EMD(price)
emd.save_figure('GOOG')
emd.plot(type='modes') # trend, all, modes, ds

# Calc The SD
sdv = SDS(price)
value = sdv.get_standard_deviation()
print(value)

# get recent News
news = News('Apple')
result = news.get_result()
