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

from Utils.FileUtil import list2dataframe
from Utils.ExperimentUtils import apply2

def compliance(p, k):
    pass


def penalty_1(p, k):
    pass


def penalty_2(p, k):
    pass


def compliance_rate_penalty(p, k):
    pass


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
    "Compute Thresholds"

    if isinstance(test, list):
        test = list2dataframe(test)

    if isinstance(test, basestring):
        test = list2dataframe([test])

    if isinstance(train, list):
        train = list2dataframe(train)

    "Apply Plans Sequentially"
    buggy = [test.iloc[n].values.tolist() for n in xrange(test.shape[0]) if
             test.iloc[n][-1] > 0]
    modified = []
    for attr in buggy:
        modified.append(apply2(changes, attr))

    modified = pd.DataFrame(modified, columns=train.columns)
    return modified
