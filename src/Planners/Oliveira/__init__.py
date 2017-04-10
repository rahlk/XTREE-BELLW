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

import numpy as np
import pandas as pd
from pdb import set_trace
from random import random as rand
from Utils.ExperimentUtils import apply3, Changes
from Utils.FileUtil import list2dataframe


def get_percentiles(df):
    percentile_array = []
    for i in np.arange(0, 1, 0.01):
        q = {col: df[col].quantile(i) for col in df.columns}
        elements = dict()
        for col in df.columns:
            try:
                elements.update({col: df.loc[df[col] >= q[col]].median()[col]})
            except:
                set_trace()

        percentile_array.append(elements)

    return percentile_array


def oliveira(train, test):
    """
    Implements shatnavi's threshold based planner.
    :param train: 
    :param test: 
    :param rftrain: 
    :param tunings: 
    :param verbose: 
    :return: 
    """
    "Helper Functions"

    def compliance_rate(k, train_columns):
        return \
            len([t for t in train_columns if t <= k]) / len(train_columns)

    def penalty_1(p, k, Min, compliance):

        comply = Min - compliance
        if comply >= 0:
                return (Min - comply) / Min
        else:
            return 0

    def penalty_2(k, Med):
        if k > Med:
            return (k - Med) / Med
        else:
            return 0

    "Compute Thresholds"

    if isinstance(test, list):
        test = list2dataframe(test)

    if isinstance(test, basestring):
        test = list2dataframe([test])

    if isinstance(train, list):
        train = list2dataframe(train)

    lo, hi = train.min(), train.max()
    quantile_array = get_percentiles(train)
    changes =[]

    pk_best = dict()

    for metric in train.columns:
        min_comply = 10e32
        vals = np.empty([10, 100])
        for p_id, p in enumerate(np.arange(0, 100, 10)):
            for k_id, k in enumerate(np.linspace(lo[metric], hi[metric], 100)):
                med = quantile_array[90][metric]
                compliance = compliance_rate(k, train[metric])
                penalty1 = penalty_1(p, k, compliance=compliance, Min=0.9)
                penalty2 = penalty_2(k, med)
                comply_rate_penalty = penalty1 + penalty2
                vals[p_id,k_id] = comply_rate_penalty

                if comply_rate_penalty <= min_comply:
                    min_comply = comply_rate_penalty
                    try:
                        pk_best[metric] = (p, k)
                    except KeyError:
                        pk_best.update({metric: (p, k)})

    """
    Apply Plans Sequentially
    """

    modified = []
    for n in xrange(test.shape[0]):
        C = Changes()
        if test.iloc[n][-1] > 0 or test.iloc[n][-1] == True:
            new_row = apply3(test.iloc[n].values.tolist(), test.columns, pk_best)
            for name, new, old in zip(test.columns, new_row, test.iloc[n].values.tolist()):
                C.save(name, new=new, old=old)

            changes.append(C.log)
            modified.append(new_row)

        # Disable the next two line if you're measuring the number of changes.
        else:
            if rand() > 0.7:
                modified.append(test.iloc[n].tolist())

    return pd.DataFrame(modified, columns=test.columns), changes

