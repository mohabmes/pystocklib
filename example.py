from pystocklib import *

# Get the historical data
hist = HistoricalData('AAPL', from_date=[2018, 1, 1], to_date=[2018, 3, 3])
price = hist.retrieve_col_data('close')
plot(price)
hist.create_csv('AAPL')


# Apply EMD & show the figure
emd = EMD(np.asarray(price))
emd.plot_imf(type='all')
emd.save_trend_figure('aapl-trend')


# Calc The SD
sdv = SDS(price)
value = sdv.get_standard_deviation()
print(value)

# get recent News
news = News('Apple')
result = news.get_result()
