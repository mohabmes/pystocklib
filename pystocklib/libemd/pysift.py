# -*- coding: utf-8 -*-
# Author: Richard Berry (c) 2017 - github.com/rjsberry/libemd
#
# This file is a part of libemd.
# libemd is licensed under the simplified BSD license.
# See LICENSE.txt for more info.

import numpy as np
from scipy import interpolate
from scipy.signal import argrelmax
from scipy.signal import argrelmin


def get_sifter(x, method=('sn', 1), **kwargs):
    """
    Class factory to instantiate a subclass of Sifter based on `method`.

    This is the public interface to sifting process class creation.
    """
    method_table = {
        'sd': {'class': SiftStopStdDev, 'optlen': 1},
        'sn': {'class': SiftStopSNum, 'optlen': 1},
        'tm': {'class': SiftStopThresh, 'optlen': 3}
    }
    opts = None

    # Split method tuple if it exists
    if isinstance(method, tuple):
        opts = method[1:]
        method = method[0]

    # Return the correct instance of a sub-class of SiftMaster
    try:
        if opts is not None:
            if len(opts) != method_table[method]['optlen']:
                errormsg = "Stoping criterion options '{}' are invalid".format(
                    opts
                )
                raise ValueError(errormsg)
            else:
                return method_table[method]['class'](*opts, x=x, **kwargs)
        else:
            return method_table[method]['class'](x=x, **kwargs)
    except KeyError:
        errormsg = "'{}' is not a valid stopping criterion".format(method)
        raise ValueError(errormsg)


class SiftMaster(object):

    stopping_criterion = None

    def __init__(
            self, x=None, t=None, max_iterations=1000,
            peakfilter=None, peakfindermax=None, peakfindermin=None):
        """
        Set parameters which are constant for any sifting process.
        """
        # The original signal
        if isinstance(x, np.ndarray):
            self._h0 = x
        else:
            raise ValueError
        # The corresponding time array
        if isinstance(t, np.ndarray):
            self.t = t
        elif t == None:
            self.t = np.arange(x.size)
        else:
            raise ValueError
        # Maximum iterations in the process
        self.max_iterations = max_iterations
        # The filter used before peak finding
        if callable(peakfilter):
            self.peakfilter = peakfilter
        elif peakfilter is None:
            self.peakfilter = lambda x: x
        else:
            raise ValueError
        # The function to locate maxima
        if callable(peakfindermax):
            self.peakfindermax = peakfindermax
        elif peakfindermax is None:
            self.peakfindermax = argrelmax
        else:
            raise ValueError
        # The function to locate minima
        if callable(peakfindermin):
            self.peakfindermin = peakfindermin
        elif peakfindermin is None:
            self.peakfindermin = argrelmin
        else:
            raise ValueError
        # Attributes used within the main sifting process loop
        # These are intended to be private; they are not set externally,
        # and should only ever be modified by methods that store data in
        # them to communicate between iterations
        self._i = None  # The iteration number
        self._h = None  # The IMF candidate
        self._i_max = None  # The indices of signal maxima
        self._i_min = None  # The indices of signal minima
        self._e_x_upper = None  # Maxima amplitudes
        self._e_x_lower = None  # Minima amplitudes
        self._e_t_upper = None  # Maxima locations in time
        self._e_t_lower = None  # Minima locations in time
        self._env_upper = None  # Upper envelope across t
        self._env_lower = None  # Lower envelope across t
        self._env_mean = None  # Mean of upper and lower envelopes across t

    @property
    def stopping_criterion_options(self):
        raise NotImplementedError

    def sift(self):
        """
        The sifting process itself.

        This is a simple for loop over the maximum allowed number
        of iterations in the sifting process that executes the
        methods defined in this class in a set order, then returns
        the decomposed IMF.
        """
        for i in range(self.max_iterations):
            self._i = i
            self.locate_extrema()
            self.set_envelope_endpoints()
            self.set_envelopes()
            self.generate_component()
            self.prep_stopsift_params()
            if self.stopsift():
                break
            else:
                self.prepare_next_iteration()
        return self._h

    def stopsift(self):
        """
        Sifting process stopping criterion. Overridden in subclasses.
        """
        raise NotImplementedError

    def locate_extrema(self):
        """
        Finds the indices of extrema for the current iteration.
        """
        self._i_max = self.extrema_indices(
            self._h0, self.peakfilter, self.peakfindermax
        )
        self._i_min = self.extrema_indices(
            self._h0, self.peakfilter, self.peakfindermin
        )
        self._e_x_upper = self._h0[self._i_max]
        self._e_x_lower = self._h0[self._i_min]
        self._e_t_upper = self.t[self._i_max]
        self._e_t_lower = self.t[self._i_min]

    @staticmethod
    def extrema_indices(x, preprocessingfilter, peakfinder):
        """
        Finds the indices of the extrema within a signal.
        """
        extrema_inds = peakfinder(preprocessingfilter(x))
        if isinstance(extrema_inds, tuple):
            extrema_inds = extrema_inds[0]
        return np.hstack([0, extrema_inds, x.size - 1])

    def set_envelope_endpoints(self):
        """
        Sets the envelope endpoints for the current iteration.
        """
        self._e_x_upper = self.endpoints(
            self._e_x_upper, self._e_t_upper, np.greater
        )
        self._e_x_lower = self.endpoints(
            self._e_x_lower, self._e_t_lower, np.less
        )

    def endpoints(self, e_x, e_t, compare):
        """
        Return an extrema array with corrected endpoints.
        """
        if e_x.size <= 2:
            return e_x
        e_x_l = self.extrapolate(e_x[1], e_t[1], e_x[2], e_t[2], e_t[0])
        e_x_r = self.extrapolate(e_x[-3], e_t[-3], e_x[-2], e_t[-2], e_t[-1])
        if compare(e_x_l, e_x[0]):
            e_x[0] = e_x_l
        if compare(e_x_r, e_x[-1]):
            e_x[-1] = e_x_r
        return e_x

    @staticmethod
    def extrapolate(x0, t0, x1, t1, t):
        """
        Finds the value of `x` at `t` via linear extrapolation.
        """
        return x0 + (x1 - x0) * (t - t0) / (t1 - t0)

    def set_envelopes(self):
        """
        Sets envelopes by fitting splines over extrema arrays.
        """
        self._env_upper = self.fit_splines(
            self._e_x_upper, self._e_t_upper, self.t
        )
        self._env_lower = self.fit_splines(
            self._e_x_lower, self._e_t_lower, self.t
        )
        self._env_mean = (self._env_upper + self._env_lower) / 2

    @staticmethod
    def fit_splines(x_array, t_array, t_new):
        """
        Fits splines between points in a range.
        """
        if x_array.size == 0 or x_array.size == 1:
            return x_array
        elif x_array.size == 2:
            tck = interpolate.splrep(t_array, x_array, k=1)
        elif x_array.size == 3:
            tck = interpolate.splrep(t_array, x_array, k=2)
        else:
            tck = interpolate.splrep(t_array, x_array, k=3)
        return interpolate.splev(t_new, tck, der=0)

    def generate_component(self):
        """
        Sets the trial IMF.
        """
        self._h = self._h0 - self._env_mean

    def prep_stopsift_params(self):
        """
        Sets instance variables required to solve the stop criterion.
        """
        raise NotImplementedError

    def prepare_next_iteration(self):
        """
        Sets "previous iteration" parameters.
        """
        self._h0 = self._h


class SiftStopStdDev(SiftMaster):

    stopping_criterion = 'sd'

    def __init__(self, sdlimit=0.3, **kwargs):
        super().__init__(**kwargs)
        # Standard deviation specific attributes
        self.sdlimit = sdlimit
        self._sd = None

    @property
    def stopping_criterion_options(self):
        return {'sdlimit': self.sdlimit}

    def prep_stopsift_params(self):
        self.set_sd()

    def set_sd(self):
        """
        Sets the standard deviation for the current iteration.
        """
        self._sd = self.get_sd(self._h0, self._h)

    @staticmethod
    def get_sd(x0, x):
        """
        Calculates the standard deviation between two signals.
        """
        return np.sum(np.abs(x0 - x)**2) / np.sum(x0**2)

    def stopsift(self):
        """
        Standard deviation sifting process stopping criterion.

        Ends the sifting process when the standard deviation of the
        current and previous IMF candidates falls below the SD limit.
        """
        if self._i == 0:
            return
        if self._sd < self.sdlimit:
            return True


class SiftStopSNum(SiftMaster):

    stopping_criterion = 'sn'

    def __init__(self, snumber=2, **kwargs):
        super().__init__(**kwargs)
        # S-number specific attributes
        self.snumber = snumber
        self._scount = 0
        self._num_zc = 0
        self._num_max = 0
        self._num_min = 0
        self._num_zc0 = 0
        self._num_max0 = 0
        self._num_min0 = 0
        self._extrema_sum = 0

    @property
    def stopping_criterion_options(self):
        return {'snumber': self.snumber}

    def prep_stopsift_params(self):
        self.count_extrema()
        self.set_extrema_sum()

    def count_extrema(self):
        self._num_zc = np.sum((self._h0[:-1] * self._h0[1:]) < 0)
        self._num_max = max(0, self._e_x_upper.size - 2)
        self._num_min = max(0, self._e_x_lower.size - 2)

    def set_extrema_sum(self):
        """
        The sum of the difference of extrema from the last iteration.
        """
        self._extrema_sum =\
            np.abs(self._num_zc - self._num_zc0) +\
            np.abs(self._num_max - self._num_max0) +\
            np.abs(self._num_min - self._num_min0)

    def stopsift(self):
        """
        S-number sifting process stopping criterion.

        Ends the sifting process if the consecutive number of iterations
        wherein the number of maxima, minima, and zero crossings have
        not changed by at most, one, is greater than the S-number.
        """
        if self._i == 0:
            return
        if self._extrema_sum <= 1:
            self._scount += 1
            if self._scount > self.snumber:
                return True
        else:
            self._scount = 0

    def prepare_next_iteration(self):
        super().prepare_next_iteration()
        self._num_zc0 = self._num_zc
        self._num_max0 = self._num_max
        self._num_min0 = self._num_min


class SiftStopThresh(SiftMaster):

    stopping_criterion = 'tm'

    def __init__(self, theta1=0.05, theta2=0.5, alpha=0.05, *args, **kwargs):
        super().__init__(**kwargs)
        # Threshold specific attributes
        # Attributes which are None are changed within the sift method
        self.theta1 = theta1
        self.theta2 = theta2
        self.alpha = alpha
        self._sigma = None

    @property
    def stopping_criterion_options(self):
        return {
            'theta1': self.theta1, 'theta2': self.theta2, 'alpha': self.alpha
        }

    def prep_stopsift_params(self):
        self.set_evaluation_function()

    def set_evaluation_function(self):
        """
        The mean envelope divided by the mode amplitude.
        """
        a = np.mean(np.abs(self._env_upper - self._env_lower)) / 2
        self._sigma = np.abs(self._env_mean) / a

    def stopsift(self):
        """
        Threshold sifting process stopping criterion.

        Ends the sifting process either when a duration of the
        evaluation function, sigma, is less than the first threshold,
        theta_1, or when any point in the evaluation function is
        greater than the second threshold, theta_2.
        """
        in_thresh1 = np.mean(self._sigma < self.theta1)
        in_thresh2 = self._sigma[np.where(self._sigma >= self.theta1)[0]]
        if in_thresh1 >= (1 - self.alpha) and np.all(in_thresh2 < self.theta2):
            return True
