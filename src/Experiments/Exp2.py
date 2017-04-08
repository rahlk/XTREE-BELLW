"""
Compare local learning with lessons from Bellwether
"""

from __future__ import print_function, division

import os
import sys

# Update path
root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)

from Data.DefectPrediction import DefectData
from Utils.FileUtil import list2dataframe
from XTREE import XTREE
from oracle.model import rforest, xgboost, xgboost_grid_tuned
from ExperimentUtils import pred_stats, impact
from Utils.StatsUtils.CrossVal import CrossValidation
from pdb import set_trace


def transfer_lessons(data=None):
    if data is None:
        data = DefectData.get_all_projects()["Apache"]

    for proj, paths in data.iteritems():
        "Make sure we don't test on the bellwether dataset"

        if not proj in paths.bellw:
            res = {proj[:6]: {
                "pd": [],
                "pf": [],
                "local": [],
                "bellw": []}
            }
            pred, pred2, distr, distr2 = [], [], [], []

            "If training data doesn't exist, create it."
            if "bellw" not in locals():
                bellw = list2dataframe(data[paths.bellw].data)

            for train_bellw, validation in CrossValidation.split(bellw,
                                                                 ways=2):
                train_local = list2dataframe(paths.data[:-1])
                test = list2dataframe(paths.data[-1])

                patched_local = XTREE.execute(train_local, test)
                patched_bellw = XTREE.execute(train_bellw, test)

                # How good are the patches from local lessons?
                pred, distr = xgboost(validation, patched_local)

                # How good are the patches from the bellwether lessons?
                pred2, distr2 = xgboost(validation, patched_bellw)

                # How good are the predictions
                pred3, distr3 = xgboost(validation, test)

                pred = pred_stats(before=test[test.columns[-1]],
                                  after=pred3,
                                  distr=distr3)

                res[proj[:6]]["pd"].append(pred[0])
                res[proj[:6]]["pf"].append(pred[1])

                res[proj[:6]]["local"].append(impact(test, pred))
                res[proj[:6]]["bellw"].append(impact(test, pred2))

            yield res
