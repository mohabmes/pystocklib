import numpy as np
import _emd as md
import matplotlib.pyplot as plt

#%% ---------------------------------------------------------------------------
# GENERATE A POLYNOMIAL + SINE TEST FUNCTION
N = 200
t = np.arange(200, dtype=float) - N / 2
amp = 10.0

# maybe a polynomial to start
y = t**2
fac = amp / np.max(y) #but let's make the numbers easier to read
y *= fac

# but let's give it an offset just to make sure that doesn't screw with things
y += amp / 5.0

# and now add in a sine
period = N / 10.0

phase = np.random.uniform(0.0, 2*np.pi)
y += (amp / 10.0) * np.sin(2*np.pi * t / period + phase)

#%% ---------------------------------------------------------------------------
# ADD NOISE, IF DESIRED
y += np.random.normal(0.0, amp/50.0, N)

#%% ---------------------------------------------------------------------------
# DECOMPOSE
# choose from sawtooth EMd or "standard"
#c, r = _emd._emd(t, y)
c, r = md.saw_emd(t, y)

#%% ---------------------------------------------------------------------------
# PLOT

pf, = plt.plot(t, y)
pr, = plt.plot(t, r)
pcs = plt.plot(t, c, 'k-')


# hist = HistoricalData()
# hist.load_csv('GOOG')
# price = hist.get_close() # 'Date', 'Open', 'High', 'Low', 'Adj', 'Close', 'Volume'
#
# x_sz = len(price)
# t = np.linspace(0, x_sz, x_sz).transpose()
# y =price
#
# c, r = emd(t, y)
#
#
# plt.figure()
# plt.plot(t, y)
#
# plt.figure()
# plt.plot(t, r)
