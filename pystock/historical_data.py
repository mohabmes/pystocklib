from .yahoo_historical import *
import datetime
path = ''


# data = Fetcher("GOOG", [2018,1,1], [2018,2,1])
# create_csv('GOOG.csv', data.getHistorical())


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




class Historical_Data:

	filename = ''
	path = ''

	data = {}
	df = ''

	from_date = ()
	to_date = ()
	stock_name = ''


	def __init__(self, stock_name, from_date=None, to_date=None):
		self.stock_name = stock_name
		self.from_date = from_date
		self.to_date = to_date
		self.date_handle()
		self.fetch()
		self.prepare_data()

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
			'Adj Close': self.df['Adj Close'].values.tolist(),
			'Volume': self.df['Volume'].values.tolist()
		}

	def get_data(self):
		return self.data


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

	def get_adjclose(self):
		return self.data['Adj Close']

	def get_volume(self):
		return self.data['Volume']

	def create_csv(self, path=''):
		self.df.to_csv(path, encoding='utf-8')




# hd = Historical_Data('GOOG')
# print(hd.get_close())

