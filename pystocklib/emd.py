"""
Created on Sat Feb 24 1:50:30 2018

@author: mohabmes

"""

# Class that utilize 'libemd' to extract trend data, plot it & save it as a image.
# libemd => Author: Richard Berry (c) 2017 - github.com/rjsberry/libemd

from .libemd.pyemd import *
from .libemd.pysift import *
import numpy as np
from matplotlib import pyplot as plt


class EMD:

	x = ()
	filename = ''
	path = ''
	imfs = ()
	t = ()

	def __init__(self, x):
		self.x = x
		# self.x = self.rev()
		# self.x = self.cutoff()
		self.calc_imfs()
		self.calc_t()



	# assuming input data is sorted DSC (ex. Date), REV() will reverse it.
	# YOU MAY NEED TO COMMENT LINE 27
	def rev(self):
		sz = len(self.x)
		result = np.zeros(sz)
		for i in range(0, sz):
			result[i] = self.x[sz - i - 1]
		return result


	# prevent list overflow
	def cutoff(self):
		if len(self.x) > 500:
			list_values = np.resize(self.x, 500)
			return list_values
		else:
			return self.x


	def calc_imfs(self):
		self.imfs = emd(self.x)


	def calc_t(self):
		x_sz = len(self.x)
		self.t = np.linspace(0, x_sz, x_sz).transpose()


	def get_trend(self):
		r, c = np.shape(self.imfs)
		if r > 1:
			return self.imfs[r-1]
		else:
			return self.imfs


	def get_figure_data(self):
		return self.get_trend(), self.t


	def save_figure(self, type='trend'):
		if type == 'trend':
			self.save_trend_figure(self.filename)
		elif type == 'all':
			self.save_all_figure(self.filename)


	def save_trend_figure(self, name):
		plt.figure()
		plt.plot(self.t, self.get_trend())
		plt.savefig('{}.png'.format(name))


	def save_all_figure(self, name):
		for i in range(0, len(self.imfs)):
			plt.figure()
			plt.plot(self.t, self.imfs[i])
			plt.savefig('{}{}.png'.format(name, i))


	def plot_imf(self, type='trend'):
		if type == 'trend':
			plt.plot(self.t, self.get_trend())
		elif type == 'all':
			for i in range(0, len(self.imfs)):
				plt.figure()
				plt.plot(self.t, self.imfs[i])
			plt.show()


	def load_csv(self):
		filename = "{}.csv".format(self.filename)
		csv = np.loadtxt(filename, delimiter=',', skiprows=1, usecols=1)
		data = np.array(csv)
		return data
