"""
XTREE
"""

from __future__ import print_function, division

import os
import sys

# Update path
root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)

import numpy as np
import pandas as pd
from ipdb import set_trace
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import f_classif
from Utils.ExperimentUtils import apply2
from Utils.FileUtil import list2dataframe


def VARL(coef, inter, p0=0.05):
    """
    :param coef: Slope of   (Y=aX+b)
    :param inter: Intercept (Y=aX+b)
    :param p0: Confidence Interval. Default p=0.05 (95%)
    :return: VARL threshold
  
              1   /     /  p0   \             \
    VARL = ----- | log | ------ | - intercept |
           slope \     \ 1 - p0 /             /
  
    """
    return (np.log(p0 / (1 - p0)) - inter) / coef


def shatnawi(train, test):
    """
    Implements shatnavi's threshold based planner.
    :param train: 
    :param test: 
    :param rftrain: 
    :param tunings: 
    :param verbose: 
    :return: 
    """
    "Compute Thresholds"

    if isinstance(test, list):
        test = list2dataframe(test)

    if isinstance(test, basestring):
        test = list2dataframe([test])

    if isinstance(train, list):
        train = list2dataframe(train)

    metrics = [str[1:] for str in train[train.columns[:-1]]]
    ubr = LogisticRegression()  # Init LogisticRegressor
    X = train[
        train.columns[:-1]]  # Independent Features (CK-Metrics)
    y = train[train.columns[-1]]  # Dependent Feature (Bugs)

    ubr.fit(X, y.values.tolist())  # Fit Logit curve
    inter = ubr.intercept_[0]  # Intercepts
    coef = ubr.coef_[0]  # Slopes
    pVal = f_classif(X, y)[1]  # P-Values
    changes = len(metrics) * [-1]

    "Find Thresholds using VARL"
    for Coeff, P_Val, idx in zip(coef, pVal,
                                 range(len(metrics))):  # xrange(len(metrics)):
        thresh = VARL(Coeff, inter, p0=0.065)  # VARL p0=0.05 (95% CI)
        if thresh > 0 and P_Val < 0.05:
            changes[idx] = thresh

    "Apply Plans Sequentially"
    buggy = [test.iloc[n].values.tolist() for n in xrange(test.shape[0]) if
             test.iloc[n][-1] > 0]
    modified = []
    for attr in buggy:
        modified.append(apply2(changes, attr))

    modified = pd.DataFrame(modified, columns=train.columns)
    return modified
