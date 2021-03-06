#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, smma


class truerange(Indicator):
    '''
    Defined by J. Welles Wilder, Jr. in 1978 in his book New Concepts in
    Technical Trading Systems.

    Formula:
      - max(high - low, abs(high - prev_close), abs(prev_close - low)

      which can be simplified to

      - truerange = max(high, prev_close) - min(low, prev_close)

    See:
      - http://en.wikipedia.org/wiki/Average_true_range

    The idea is to take the previous close into account to calculate the range
    if it yields a larger range than the daily range (High - Low)
    '''
    group = 'volatility'
    alias = 'TR', 'TrueRange', 'trange', 'TRANGE'
    inputs = 'high', 'low', 'close'
    outputs = 'tr'
    params = (
        ('period', 14, 'Period to consider'),
    )

    def __init__(self):
        close1 = self.i.close.shift(periods=1)
        truehi = close1.clip(lower=self.i.high)  # max of close(-1) and hi
        truelo = close1.clip(upper=self.i.low)  # min of close(-1) and low
        self.o.tr = truehi - truelo


class atr(truerange, outputs_override=True):
    '''
    Defined by J. Welles Wilder, Jr. in 1978 in his book *"New Concepts in
    Technical Trading Systems"*.

    The idea is to take the close into account to calculate the range if it
    yields a larger range than the daily range (High - Low)

    Formula:
      - truerange = max(high, close(-1)) - min(low, close(-1))
      - atr = SmoothedMovingAverage(truerange, period)

    See:
      - http://en.wikipedia.org/wiki/Average_true_range
    '''
    group = 'volatility'
    alias = 'ATR', 'AverageTrueRange'
    # outputs = {'atr': 'tr'}  # define atr / alias tr to it for the base class
    outputs = 'atr'  # notice outputs_override, adds autoalias to output tr
    params = (
        ('_ma', smma, 'Moving average to use'),
    )

    def __init__(self):
        self.o.atr = self.p._ma(self.o.tr, period=self.p.period)
