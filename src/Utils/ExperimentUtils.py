from __future__ import print_function, division

import os
import sys

# Update path
root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)

from random import uniform
from Utils.StatsUtils.ABCD import abcd


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
