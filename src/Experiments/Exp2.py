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
from Planners.XTREE import xtree
from oracle.model import xgboost
from Utils.ExperimentUtils import pred_stats, impact
from Utils.StatsUtils.CrossVal import CrossValidation


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

            bellw = list2dataframe(data[paths.bellw].data)

            for train_bellw, validation in CrossValidation.split(bellw,
                                                                 ways=5):
                train_local = list2dataframe(paths.data[:-1])
                test = list2dataframe(paths.data[-1])

                patched_local = xtree(train_local, test)
                patched_bellw = xtree(train_bellw, list2dataframe(paths.data))

                # How good are the patches from local lessons?
                pred_local, distr_local = xgboost(validation, patched_local)

                # How good are the patches from the bellwether lessons?
                pred_bellw, distr_bellw = xgboost(validation, patched_bellw)

                # How good are the predictions
                pred_qual, distr_qual = xgboost(validation, test)

                pred = pred_stats(before=test[test.columns[-1]],
                                  after=pred_qual,
                                  distr=distr_qual)

                res[proj[:6]]["pd"].append(pred[0])
                res[proj[:6]]["pf"].append(pred[1])

                res[proj[:6]]["local"].append(impact(test, pred_local))
                res[proj[:6]]["bellw"].append(impact(test, pred_bellw))

            yield res
