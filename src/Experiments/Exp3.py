"""
Compare Bellwether XTREEs with other threshold based learners.
"""

from __future__ import print_function, division

import os
import sys

# Update path
root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)

import numpy as np
from pdb import set_trace
from Data.DefectPrediction import DefectData
from Utils.FileUtil import list2dataframe
from Planners.XTREE import xtree
from Planners.Shatnawi import shatnawi
from Planners.Alves import alves
from Planners.Oliveira import oliveira
from Planners.Fontana import fontana

from oracle.model import rforest, xgboost
from Utils.ExperimentUtils import pred_stats, impact
from Utils.StatsUtils.CrossVal import CrossValidation


def transfer_lessons(data=None):
    if data is None:
        data = DefectData.get_all_projects()["Apache"]

    for proj, paths in data.iteritems():
        "Make sure we don't test on the bellwether dataset"

        if not proj in paths.bellw:
            res = {proj[:6]: {
                "xtree": [],
                "alves": [],
                "shatw": []}
            }

            bellw = list2dataframe(data[paths.bellw].data)

            for train_bellw, validation in CrossValidation.split(bellw,
                                                                 ways=2):
                test = list2dataframe(paths.data)

                patched_alves = alves(train_bellw, test)
                patched_shatw = shatnawi(train_bellw, test)
                patched_xtree = xtree(train_bellw, test)

                # How good are the patches from local lessons?
                pred_alves, distr_alves = xgboost(validation, patched_alves)

                # How good are the predictions
                pred_shatw, distr_shatw = xgboost(validation, patched_shatw)

                # How good are the patches from the bellwether lessons?
                pred_xtree, distr_xtree = xgboost(validation, patched_xtree)

                res[proj[:6]]["xtree"].append(impact(test, pred_xtree))
                res[proj[:6]]["alves"].append(impact(test, pred_alves))
                res[proj[:6]]["shatw"].append(impact(test, pred_shatw))

                # Not yet...
                #
                # # How good are the patches from the bellwether lessons?
                # pred_oliveira, distr_oliveira = xgboost(validation, patched_xtree)
                #
                # # How good are the patches from the bellwether lessons?
                # pred_fontana, distr_fontana = xgboost(validation, patched_xtree)
                #
                # # res[proj[:6]]["oliveira"].append(pred[1])
                # # res[proj[:6]]["fontana"].append(pred[1])

            yield res


if __name__ == "__main__":
    for res in transfer_lessons():
        for key, value in res.iteritems():
            print(key
                  , np.median(value["xtree"], axis=0)
                  , np.percentile(value["xtree"], 25, axis=0)
                  , np.percentile(value["xtree"], 75, axis=0)
                  , np.median(value["alves"], axis=0)
                  , np.percentile(value["alves"], 25, axis=0)
                  , np.percentile(value["alves"], 75, axis=0)
                  , np.median(value["shatw"], axis=0)
                  , np.percentile(value["shatw"], 25, axis=0)
                  , np.percentile(value["shatw"], 75, axis=0)
                  , sep="\t")
    # print("")
    set_trace()
