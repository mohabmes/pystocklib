"""
Created on Sat Feb 24 1:50:30 2018

@author: mohabmes

"""

# Class that utilize 'emd' to extract trend data, plot it & save it as a image.
# emd => Author: R. O. Parke Loyd - https://github.com/parkus/emd

from .emd_lib import *
import numpy as np
# from matplotlib import pyplot as plt
from .visual import plot_fig, plot_figs, save_fig

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
		elif type == 'ds':
			self.save_all_figure(filename)


	def save_trend_figure(self, name):
		save_fig(self.t, self.get_trend(), '{}'.format(name))


	def save_all_figure(self, name):
		pf, = plt.plot(self.t, self.x)
		pr, = plt.plot(self.t, self.get_trend())

		plt.legend((pf, pr), ('Price', 'Trend'))
		plt.savefig('{}.png'.format(name))


	def plot(self, type='trend'):
		if type == 'trend':
			plot_fig(self.t, self.get_trend())
		elif type == 'all':
			plot_figs([
						[self.t, self.get_trend()],
						[self.t, self.c]
						])
		elif type == 'modes':
			sz = len(self.get_modes())
			imfs_sz = len(self.c[0])
			t = np.linspace(0, imfs_sz, imfs_sz).transpose()
			for i in range(0, sz, 500):
				plt.figure()
				plt.plot(t, self.c[i])
			plt.show()
		elif type == 'ds':
			pf, = plt.plot(self.t, self.x)
			pr, = plt.plot(self.t, self.get_trend())

			plt.legend((pf, pr), ('original function', 'residual'))
			plt.show()

