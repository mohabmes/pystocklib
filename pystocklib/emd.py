"""
Created on Sat Feb 24 1:50:30 2018

@author: mohabmes

"""

# Class that utilize 'emd' to extract trend data, plot it & save it as a image.
# emd => Author: R. O. Parke Loyd - https://github.com/parkus/emd

from .emd_lib import *
import numpy as np
from matplotlib import pyplot as plt


class EMD:

	x = ()
	filename = ''
	path = ''
	c = ()
	r = ()
	t = ()

	def __init__(self, x, last_month=None):
		self.x = x
		# self.x = self.rev()
		if last_month is not None:
			self.x = self.cutoff(last_month)
		self.calc_t()
		self.emd()

		# print(self.r)
		# print(self.c)




	# assuming input data is sorted DSC (ex. Date), REV() will reverse it.
	# YOU MAY NEED TO COMMENT LINE 27
	def rev(self):
		sz = len(self.x)
		result = np.zeros(sz)
		for i in range(0, sz):
			result[i] = self.x[sz - i - 1]
		return result


	def cutoff(self, last_month):
		if len(self.x) > last_month*30:
			list_values = np.resize(self.x, last_month*30)
			return list_values
		else:
			return self.x


	def emd(self):
		c, r = emd(self.t, self.x)
		self.c = c
		self.r = r


	def calc_t(self):
		x_sz = len(self.x)
		self.t = np.linspace(0, x_sz, x_sz).transpose()


	def get_trend(self):
		return self.r


	def get_modes(self):
		return self.c


	def save_figure(self, filename, type='trend'):
		if type == 'trend':
			self.save_trend_figure(filename)
		elif type == 'all':
			self.save_all_figure(filename)
		elif type == 'ds':
			pf, = plt.plot(self.t, self.x)
			pr, = plt.plot(self.t, self.r)
			pcs = plt.plot(self.t, self.c, 'k-')

			plt.legend((pf, pcs[0], pr), ('original function', 'modes', 'residual'))
			plt.savefig('{}.png'.format(filename))


	def save_trend_figure(self, name):
		plt.figure()
		plt.plot(self.t, self.get_trend())
		plt.savefig('{}.png'.format(name))


	def save_all_figure(self, name):
		plt.figure()
		plt.plot(self.t, self.get_trend())
		plt.savefig('{}1.png'.format(name))

		plt.figure()
		plt.plot(self.t, self.c)
		plt.savefig('{}2.png'.format(name))



	def plot(self, type='trend'):
		if type == 'trend':
			plt.plot(self.t, self.get_trend())
			plt.show()
		elif type == 'all':
			plt.figure()
			plt.plot(self.t, self.get_trend())
			plt.figure()
			plt.plot(self.t, self.c)
			plt.show()
		elif type == 'modes':
			sz = len(self.get_modes())
			for i in range(0, sz, 500):
				sz = len(self.c[i])
				t = np.linspace(0, sz, sz).transpose()
				plt.figure()
				plt.plot(t, self.c[i])
			plt.show()
		elif type == 'ds':
			pf, = plt.plot(self.t, self.x)
			pr, = plt.plot(self.t, self.r)
			pcs = plt.plot(self.t, self.c, 'k-')

			plt.legend((pf, pcs[0], pr), ('original function', 'modes', 'residual'))
			plt.show()


	def load_csv(self):
		filename = "{}.csv".format(self.filename)
		csv = np.loadtxt(filename, delimiter=',', skiprows=1, usecols=1)
		data = np.array(csv)
		return data
