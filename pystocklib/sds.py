import math

class SDS:

	values = ()
	sum = 0
	mean = 0
	variance = 0
	standard_deviation = 0

	def __init__(self, values):
		self.values = values
		self.resize_arr()
		self.calc_sum()
		self.calc_mean()
		self.calc_variance()
		self.calc_standard_deviation()

	def resize_arr(self):
		sz = len(self.values)
		if sz > 30:
			self.values = self.values[(sz-31):]


	def calc_sum(self):
		self.sum = 0
		for i in self.values:
			self.sum += i


	def calc_mean(self):
		self.mean = float(self.sum) / len(self.values)


	def calc_variance(self):
		for i in self.values:
			self.variance += (i - self.mean)**2

		self.variance = float(self.variance) / len(self.values)


	def calc_standard_deviation(self):
		self.standard_deviation = math.sqrt(self.variance)

	def get_standard_deviation(self):
		return self.standard_deviation
