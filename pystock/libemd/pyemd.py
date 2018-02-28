# -*- coding: utf-8 -*-
# Author: Richard Berry (c) 2017 - github.com/rjsberry/libemd
#
# This file is a part of libemd.
# libemd is licensed under the simplified BSD license.
# See LICENSE.txt for more info.

import numpy as np

from .pysift import get_sifter


def emd(x, *args, **kwargs):
    """
    Main empirical mode decomposition signal routine.
    """
    # Setup some initial parameters
    n = x.shape[0]
    m = num_imfs(n)
    imfs = np.zeros([m, n])

    # The main EMD loop
    for i in range(m):
        if i == 0:
            r = x
        if is_monotonic(r):
            imfs[i] = r
            break
        imf = get_sifter(r, *args, **kwargs).sift()
        imfs[i] = imf
        r = r - imf

    # Get data ready to be returned to user
    imfs = np.delete(imfs, np.s_[i+1: ], 0)
    if imfs.shape[0] == 1:
        return imfs.flatten()
    else:
        return imfs


def num_imfs(n):
    """
    Guesses a maximum number of IMFs based on signal length.
    """
    if n == 0:
        return 0
    elif n <= 3:
        return 1
    else:
        return int(np.floor(np.log2(n)))


def is_monotonic(x):
    """
    Returns True if `x` is monotonic, otherwise returns False.
    """
    if np.all(np.diff(x) >= 0):
        return True
    elif np.all(np.diff(x) <= 0):
        return True
