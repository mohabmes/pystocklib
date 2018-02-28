from pystock import *

# Get the historical data
hist_data = Historical_Data('goog')
price = hist_data.get_close()
print(hist_data.get_df())


# Apply EMD & show the figure
emd = EMD(np.asarray(price))
emd.plot_imf(type='all')
emd.save_trend_figure('trend-img')


Calc The SD
sdv = SDS(price)
value = sdv.get_standard_deviation()



# get recent News
news = News('apple')
result = news.get_result()



