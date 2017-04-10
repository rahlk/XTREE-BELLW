from __future__ import print_function, division

import os
import sys

# Update path
root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)

import pandas as pd
from random import uniform
from Utils.StatsUtils.ABCD import abcd
from random import uniform as random
from pdb import set_trace
import numpy as np


def impact(test, pred):
    actuals = test[test.columns[-1]]
    gain = round(100 * (1 - sum(pred) / sum(actuals)), 2)
    return gain


def pred_stats(before, after, distr):
    pd, pf = abcd(before, after, distr)[:2]
    return round(pd, 2), round(pf, 2)


def apply(changes, row):
    all = []
    for idx, thres in enumerate(changes):
        newRow = row
        if thres > 0:
            if newRow[idx] > thres:
                newRow[idx] = uniform(0, thres)
            all.append(newRow)

    return all


def apply2(changes, row):
    newRow = row
    for idx, thres in enumerate(changes):
        if thres > 0:
            if newRow[idx] > thres:
                newRow[idx] = uniform(0, thres)

    return newRow


def apply3(row, cols, pk_best):
    newRow = row
    for idx, col in enumerate(cols):
        proba = pk_best[col][0]
        thres = pk_best[col][1]
        if thres > 0:
            if newRow[idx] > thres:
                newRow[idx] = uniform(0, thres) if random(0, 100) < proba else \
                    newRow[idx]

    return newRow


def deltas(orig, patched):
    delt_numr = []
    delt_bool = []
    for row_a, row_b in zip(orig.values[:-1], patched.values[:-1]):
        delt_bool.append([1 if a == b else 0 for a, b in zip(row_a, row_b)])

    delt_bool = np.array(delt_bool)
    fractional_change = np.sum(delt_bool, axis=0) * 100 / len(delt_bool)

    return fractional_change.tolist()


def deltas_magnitude(orig, patched):
    delt_numr = []
    delt_bool = []
    for row_a, row_b in zip(orig.values[:-1], patched.values[:-1]):
        delt_bool.append([b - a for a, b in zip(row_a, row_b)])

    delt_bool = np.array(delt_bool)
    delt_bool = np.nan_to_num((delt_bool - delt_bool.min(axis=0)) / (
    delt_bool.max(axis=0) - delt_bool.min(axis=0)))
    fractional_change = np.mean(delt_bool, axis=0)
    return fractional_change.tolist()
