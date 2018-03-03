from matplotlib import pyplot as plt


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
