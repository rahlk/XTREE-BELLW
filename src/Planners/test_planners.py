"""
Test all planners.
"""

from __future__ import print_function, division

import os
import sys

# Update path
root = os.path.join(os.getcwd().split('src')[0], "src")
if root not in sys.path:
    sys.path.append(root)

from ipdb import set_trace
from Data.DefectPrediction import DefectData
from Utils.FileUtil import list2dataframe

from Planners.XTREE import xtree
from Planners.Shatnawi import shatnawi
from Planners.Alves import alves
from Planners.Oliveira import oliveira
from Planners.Fontana import fontana

from oracle.model import rforest
from Utils.ExperimentUtils import pred_stats, impact
from Utils.StatsUtils.CrossVal import CrossValidation


def __test_alves(data):
    train, test = data.data[:-1], data.data[-1]
    alves(train, test)
    pass


def __test_shatnawi(data):
    train, test = data.data[:-1], data.data[-1]
    shatnawi(train, test)
    pass


def __test_xtree(data):
    train, test = data.data[:-1], data.data[-1]
    xtree(train, test)
    pass


def __test_oliveira(data):
    train, test = data.data[:-1], data.data[-1]
    oliveira(train, test)
    pass


def __test_fontana(data):
    train, test = data.data[:-1], data.data[-1]
    fontana(train, test)
    pass


def run_all_tests():
    data = DefectData.get_all_projects()["Apache"]["ant"]
    __test_oliveira(data)


if __name__ == "__main__":
    run_all_tests()
