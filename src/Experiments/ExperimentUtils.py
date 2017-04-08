from __future__ import print_function, division

import os
import sys

# Update path
root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)

from Utils.StatsUtils.ABCD import abcd


def impact(test, pred):
    actuals = test[test.columns[-1]]
    gain = round(100*(1 - sum(pred) / sum(actuals)), 2)
    return gain


def pred_stats(before, after, distr):
    pd, pf = abcd(before, after, distr)[:2]
    return round(pd, 2), round(pf, 2)
