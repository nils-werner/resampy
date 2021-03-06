#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import numpy as np
import scipy.signal
import resampy

from nose.tools import eq_, raises


def test_shape():

    def __test(axis, sr_orig, sr_new, X):

        Y = resampy.resample(X, sr_orig, sr_new, axis=axis)

        target_shape = list(X.shape)
        target_shape[axis] = target_shape[axis] * sr_new // sr_orig

        eq_(target_shape, list(Y.shape))

    sr_orig = 100
    X = np.random.randn(sr_orig, sr_orig, sr_orig)

    for axis in [0, 1, 2]:
        yield __test, axis, sr_orig, sr_orig // 2, X


def test_bad_sr():

    x = np.zeros(100)
    yield raises(ValueError)(resampy.resample), x, 100, 0
    yield raises(ValueError)(resampy.resample), x, 100, -1
    yield raises(ValueError)(resampy.resample), x, 0, 100
    yield raises(ValueError)(resampy.resample), x, -1, 100


def test_bad_rolloff():

    @raises(ValueError)
    def __test(rolloff):

        x = np.zeros(100)
        resampy.resample(x, 100, 50, filter='sinc_window', rolloff=rolloff)
    
    yield __test, -1
    yield __test, 1.5


@raises(ValueError)
def test_bad_precision():

    x = np.zeros(100)
    resampy.resample(x, 100, 50, filter='sinc_window', precision=-1)
    

@raises(ValueError)
def test_bad_num_zeros():

    x = np.zeros(100)
    resampy.resample(x, 100, 50, filter='sinc_window', num_zeros=0)

def test_dtype():

    def __test(dtype):
        x = np.random.randn(100).astype(dtype)

        y = resampy.resample(x, 100, 200)

        eq_(x.dtype, y.dtype)

    yield __test, np.float32
    yield __test, np.float64


@raises(TypeError)
def test_bad_window():

    x = np.zeros(100)

    resampy.resample(x, 100, 200, filter='sinc_window', window=np.ones(50))


def test_good_window():

    sr_orig = 100
    sr_new = 200
    x = np.random.randn(500)

    y = resampy.resample(x, sr_orig, sr_new, filter='sinc_window', window=scipy.signal.blackman)

    eq_(len(y), 2 * len(x))
