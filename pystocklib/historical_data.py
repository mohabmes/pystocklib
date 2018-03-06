from .yahoo_historical import *
import datetime
from numpy import loadtxt


def monthdelta(date, delta):
	m, y = (date.month + delta) % 12, date.year + ((date.month) + delta - 1) // 12
	if not m: m = 12
	d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
	return date.replace(day=d,month=m, year=y)


def strdate_to_list(str):
	str = datetime.datetime.strftime(str, "%Y-%m-%d")

	dates_list = [int(elem) for elem in str.split('-')]
	return dates_list


class HistoricalData:
	stock_name = ''
	path = ''

	data = {}
	df = ''

	from_date = ()
	to_date = ()


	def __init__(self, stock_name=None, from_date=None, to_date=None, path=None):
		self.stock_name = stock_name
		self.from_date = from_date
		self.to_date = to_date
		self.path = path
		if self.stock_name is not None:
			self.date_handle()
			self.fetch()
			self.prepare_data()


	def load_csv(self, path):
		tmp = loadtxt('{}.csv'.format(path), delimiter=',', usecols=(range(2,8)), skiprows = 1, unpack = True)
		self.data['Open'] = tmp[0]
		self.data['High'] = tmp[1]
		self.data['Low'] = tmp[2]
		self.data['Close'] = tmp[3]
		self.data['Adj'] = tmp[4]
		self.data['Volume'] = tmp[5]

	def date_handle(self):

		if (self.from_date and self.to_date) is None:
			date_now = datetime.datetime.now().strftime("%Y-%m-%d")
			date_6month = monthdelta(datetime.datetime.strptime(date_now, "%Y-%m-%d"), -6)
			date_now = strdate_to_list(datetime.datetime.strptime(date_now, "%Y-%m-%d"))
			date_6month = strdate_to_list(date_6month)

			self.to_date = date_now
			self.from_date = date_6month

		if self.to_date is None:
			date_now = datetime.datetime.now().strftime("%Y-%m-%d")
			date_now = strdate_to_list(date_now)

			self.to_date = date_now


	def fetch(self):
		dataframe = Fetcher(self.stock_name, self.from_date, self.to_date)
		self.df = dataframe.getHistorical()

	def get_df(self):
		return self.df

	def prepare_data(self):
		self.data = {
			'Date': self.df['Date'].values.tolist(),
			'Open': self.df['Open'].values.tolist(),
			'High': self.df['High'].values.tolist(),
			'Low': self.df['Low'].values.tolist(),
			'Close': self.df['Close'].values.tolist(),
			'Adj': self.df['Adj Close'].values.tolist(),
			'Volume': self.df['Volume'].values.tolist()
		}

	def retrieve_data(self):
		return self.data

	def retrieve_col_data(self, col_num):
		# 'Date', 'Open', 'High', 'Low', 'Adj Close', 'Close', 'Volume'
		return self.data[col_num]

	def get_date(self):
		return self.data['Date']

	def get_open(self):
		return self.data['Open']

	def get_high(self):
		return self.data['High']

	def get_low(self):
		return self.data['Low']

	def get_close(self):
		return self.data['Close']

	def get_adj(self):
		return self.data['Adj']

	def get_volume(self):
		return self.data['Volume']

	def create_csv(self):
		self.df.to_csv('{}.csv'.format(self.stock_name), encoding='utf-8')

