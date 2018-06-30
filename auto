from pystocklib import *
import os
import sys
import json

stock_name = ""
path = ""


if not os.path.exists('tmpdata'):
    os.makedirs('tmpdata')


if sys.argv[0] and sys.argv[1] != "":
   stock_name = sys.argv[1]
   path = 'tmpdata/{}'.format(stock_name)

if not os.path.exists(path):
    os.makedirs(path)

# fetch Historical Data
hist = HistoricalData(stock_name, from_date=[2015, 1, 1], to_date=[2018, 6, 30], path=path)
hist.create_csv()
hist.info_plot('Open', 'Close')

# figures
price = hist.get_close()
emd = EMD(price, path=path)
emd.save_figure('{}-trend'.format(stock_name), type='trend')
emd.save_figure('{}-ds'.format(stock_name), type='ds')

# Calc standard_deviation
sd = hist.standard_deviation('Open')
with open("{}/sd.json".format(path), 'w') as outfile:
     json.dump(sd, outfile)

# get recent News
news = News(stock_name, path=path)
news.export_json()

