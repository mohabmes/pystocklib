from matplotlib import pyplot as plt
from matplotlib import style

style.use('ggplot')

def plot(values=[]):
	sz = len(values)
	plt.figure()
	plt.plot(range(0, sz), values)
	plt.show()


def save_plot(name, values=[]):
	sz = len(values)
	plt.figure()
	plt.plot(range(0, sz), values)
	plt.savefig('{}.png'.format(name))


def plot_fig(t, y):
	plt.figure()
	plt.plot(t, y)
	plt.show()


def plot_figs(figures = ()):
	for fig in figures:
		plt.figure()
		plt.plot(fig[0], fig[1])
	plt.show()


def save_fig(t, y, name):
	plt.figure()
	plt.plot(t, y)
	plt.savefig('{}.png'.format(name))


def subplot(name, v1 = (), v2 = ()):
	ax1 = plt.subplot(1, 1, 1)
	ax1.plot(v1[0], label=v1[1])
	ax1.plot(v2[0], label=v2[1])
	plt.legend()
	plt.savefig('{}.png'.format(name))


def subplot1(name, values = ()):
	ax1 = plt.subplot(1, 1, 1)
	ax1.plot(values[0], label=values[1])
	plt.legend()
	plt.savefig('{}.png'.format(name))


def subplot_info(name, values):
	ax1 = plt.subplot(2, 1, 1)
	ax1.plot(values[0][0], label=values[0][1])
	ax1.plot(values[1][0], label=values[1][1])
	plt.legend()

	ax1 = plt.subplot(2, 1, 2, sharex = ax1)
	ax1.plot(values[2][0], label=values[2][1])
	plt.legend()
	plt.savefig('{}-info.png'.format(name))
