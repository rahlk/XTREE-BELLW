"""
Deriving Metric Thresholds from Benchmark Data

Alves, T. L., Ypma, C., & Visser, J. (2010). Deriving metric thresholds from 
benchmark data. In ICSM'10 (pp. 1-10). http://doi.org/10.1109/ICSM.2010.5609747
"""

from __future__ import print_function, division

import os
import sys

# Update path
root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)

from sklearn.feature_selection import f_classif
import numpy as np
from Utils.ExperimentUtils import apply2
import pandas as pd
from ipdb import set_trace
from Utils.FileUtil import list2dataframe

def _ent_weight(X, scale):
    Y = []
    for x in X.values:
        loc = x[10]  # LOC is the 10th index position.
        Y.append([xx * loc for xx in x])
    return Y


def alves(train, test):

    if isinstance(test, list):
        test = list2dataframe(test)

    if isinstance(test, basestring):
        test = list2dataframe([test])

    if isinstance(train, list):
        train = list2dataframe(train)

    metrics = [met[1:] for met in train[train.columns[:-1]]]
    X = train[train.columns[:-1]]  # Independent Features (CK-Metrics)

    """
    As weight we will consider 
    the source lines of code (LOC) of the entity.
    """

    tot_loc = train.sum()["$loc"]
    X = _ent_weight(X, scale=tot_loc)

    """
    Divide the entity weight by the sum of all weights of the same system.
    """
    denom = pd.DataFrame(X).sum().values
    norm_sum = pd.DataFrame(pd.DataFrame(X).values / denom, columns=metrics)

    """
    Find Thresholds
    """
    y = train[train.columns[-1]]  # Dependent Feature (Bugs)
    pVal = f_classif(X, y)[1]  # P-Values
    cutoff = []
    cumsum = lambda vals: [sum(vals[:i]) for i, __ in enumerate(vals)]

    def point(array):
        for idx, val in enumerate(array):
            if val > 0.95: return idx

    for idx in xrange(len(train.columns[:-1])):
        # Setup Cumulative Dist. Func.
        name = metrics[idx]
        loc = train["$loc"].values
        vals = norm_sum[name].values
        sorted_ids = np.argsort(vals)
        cumulative = [sum(vals[:i]) for i, __ in enumerate(sorted(vals))]
        # set_trace()
        if pVal[idx] < 0.05:
            cutpoint = point(cumulative)
            cutoff.append(vals[sorted_ids[cutpoint]] * tot_loc / loc[
                sorted_ids[cutpoint]] * denom[idx])
        else:
            cutoff.append(-1)

    """ 
    Apply Plans Sequentially
    """
    n_change = len([c for c in cutoff if c > 0])
    buggy = [test.iloc[n].values.tolist() for n in xrange(test.shape[0]) if
             test.iloc[n][-1] > 0]

    modified = []

    for attr in buggy:
        try:
            modified.append(apply2(cutoff, attr))
        except:
            set_trace()

    modified = pd.DataFrame(modified, columns=train.columns)
    return modified
