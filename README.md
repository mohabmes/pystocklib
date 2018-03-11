# pystocklib
Python package for Stock Market analysis. (Historical Data, EMD Trend signal, News extraction, News analysis, etc..)

# How to use

Get the historical data
```

hist = HistoricalData('AAPL', from_date=[2005, 1, 1], to_date=[2018, 3, 1])

price = hist.get_high()

# or use: hist.retrieve_col_data('Open') 'Date', 'Open', 'High', 'Low', 'Adj', 'Close', 'Volume'

```
#### Output
```
            Date        Open        High         Low       Close   Adj Close      Volume
0     2007-01-03   12.327143   12.368571   11.700000   10.812462   11.971429   309579900
1     2007-01-04   12.007143   12.278571   11.974286   11.052453   12.237143   211815100
2     2007-01-05   12.252857   12.314285   12.057143   10.973743   12.150000   208685400
3     2007-01-08   12.280000   12.361428   12.182858   11.027935   12.210000   199276700
4     2007-01-09   12.350000   13.282857   12.164286   11.944029   13.224286   837324600
5     2007-01-10   13.535714   13.971429   13.350000   12.515617   13.857142   738220000
6     2007-01-11   13.705714   13.825714   13.585714   12.360788   13.685715   360063200
7     2007-01-12   13.512857   13.580000   13.318571   12.208535   13.517143   328172600
```



Plot & Generate CSV file
```

hist.create_csv()

plot(price)

```
#### Output
[CSV File](https://github.com/mohabmes/pystocklib/blob/master/data/AAPL.csv)<br>
![AAPL-data.png](./data/AAPL-data.png)



Load data from csv file
```

hist = HistoricalData()

hist.load_csv('AAPL')

hist.info_plot('Close')

```
#### Output
![AAPL info](./data/AAPL-info.png)


Apply EMD & show the figure
```

emd = EMD(price)

emd.save_figure('AAPL-trend', type='trend') # type => trend, all, modes, ds

```
#### Output
![AAPL-trend](./data/AAPL-trend.png)


Calc The SD
```

sdv = hist.standard_deviation('Open')

print(sdv)

```
#### Output
```
if 0 < sdv < 25
	then it will be considered as 'SAFE'
Otherwise
	it's 'RISKY'

```


Gather News & analysis it
```

news = News('Apple')

result = news.get_result()

```
#### Output
```
{
	'news': [
		{
			'text': 'Apple May Be Working on High-End Headphones and a Cheaper MacBook Air',
			'a': 'http://fortune.com/2018/03/10/apple-headphones-macbook-air/',
			'website': 'fortune.com',
			'sentiment': 0.6
		},
		{
			'text': "Apple's 14 Week December 2016 Quarter Seems To Have Confused A Lot Of People",
			'a': 'https://www.forbes.com/sites/chuckjones/2018/03/09/apples-14-week-december-2016-quarter-seems-to-have-confused-a-lot-of-people/',
			'website': 'forbes.com',
			'sentiment': -0.4
		}
		...
		...
		...
	],
	'sentiment': 0.019337121212121215
}

```

# Credit
- [AndrewRPorter](https://github.com/AndrewRPorter)
- [parkus](https://github.com/parkus)

# License
[MIT License](https://github.com/mohabmes/pystocklib/blob/master/LICENSE) Copyright (c) 2018 mohabmes
