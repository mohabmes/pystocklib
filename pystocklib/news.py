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

	def __init__(self, topic):
		self.topic = topic
		self.get_markup()
		self.extract_news()
		self.calc_sentiment()


	def get_markup(self):

		url = 'https://news.google.com/news/search/section/q/{}'.format(self.topic)

		resp = requests.get(url, allow_redirects=True)
		src_code = resp.text.encode('ascii', 'replace')
		self.bs = BeautifulSoup(src_code, "html.parser")


	def extract_news(self):
		all_news_markup = self.bs.find("div", {"class": "deQdld"})

		for ch in all_news_markup.findAll("c-wiz", {"class": "PaqQNc"}):

			for item in ch.findAll("a", {"class": "nuEeue", "aria-level": "2"}):
				news = {
					"text": item.text,
					"a": item.get('href'),
					"website": get_tld(item.get('href')),
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




# news = News('Google')
# all = news.get_result()
# print(all)
# print(news.get_sentiment())
