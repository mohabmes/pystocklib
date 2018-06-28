import requests
from bs4 import BeautifulSoup
from tld import get_tld
from textblob import TextBlob


class News:

	all_news = []
	topic = ''
	bs = ''
	sentiment = 0
	result = {}
	path = ""

	def __init__(self, topic, path=None):
		self.topic = topic
		self.path = path
		self.get_markup()
		self.extract_news()
		self.calc_sentiment()


	def get_markup(self):

		url = 'https://news.google.com/search?q={}'.format(self.topic)
		resp = requests.get(url, allow_redirects=True)
		src_code = resp.text.encode('ascii', 'replace')
		self.bs = BeautifulSoup(src_code, "html.parser")


	def extract_news(self):
		all_news_markup = self.bs.find("div", {"class": "lBwEZb BL5WZb xP6mwf"})

		for ch in all_news_markup.findAll("div", {"jsmodel": "zT6vwb"}):

			for item in ch.findAll("a", {"class": "ipQwMb Q7tWef"}):
				href = item.get('href')
				href = href.replace('./', 'https://news.google.com/')
				news = {
					"text": item.text,
					"a": href,
					"sentiment": self.sentiment(item.text)
				}

			if item is not None:
				self.all_news.append(news.copy())


	@staticmethod
	def sentiment(str):
		blob = TextBlob(str)
		return blob.sentiment.polarity


	def calc_sentiment(self):
		result = 0
		cnt = 0

		for news in self.all_news:
			alpha = 0
			if news['sentiment'] > 0:
				cnt +=1
				alpha = 1
			elif news['sentiment'] < 0:
				cnt += 1
			result += alpha

		self.sentiment = result
		self.sentiment = float(result) / cnt


	def get_sentiment(self):
		return round(self.sentiment * 100, 2)


	def get_news(self):
		return self.all_news

	def get_result(self):
		return {
			'news': self.get_news(),
			'sentiment': self.get_sentiment()
		}

	def export_json(self):
		import json
		with open('{}-news.json'.format(self.path+'/'+self.topic), 'w') as outfile:
			json.dump(self.get_result(), outfile)
