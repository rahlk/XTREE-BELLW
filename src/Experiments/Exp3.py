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

        if proj in ["ant", "ivy", "poi", "jedit"]:
            res = {proj[:6]: {
                "xtree_local": [],
                "xtree_bellw": [],
                "alves": [],
                "olive": [],
                "shatw": []}
            }

            bellw = list2dataframe(data[paths.bellw].data)
            test = list2dataframe(paths.data)
            test_local = list2dataframe(paths.data[-1])
            train_local = list2dataframe(paths.data[:-1])

            for train_bellw, validation in CrossValidation.split(bellw,
                                                                 ways=5):
                patched_alves = alves(train_bellw, test_local)
                patched_shatw = shatnawi(train_bellw, test_local)
                patched_olive = oliveira(train_bellw, test_local)
                patched_xtree = xtree(train_bellw, test_local)
                patched_xtree_local = xtree(train_local, test_local)

                # How good are the patches from Alves?
                pred_alves, distr_alves = xgboost(validation, patched_alves)

                # How good are the patches from Shatnawi?
                pred_shatw, distr_shatw = xgboost(validation, patched_shatw)

                # How good are the patches from Oliveira?
                pred_olive, distr_olive = xgboost(validation, patched_olive)

                # How good are the patches from the bellwether XTREE?
                pred_xtree, distr_xtree = xgboost(validation, patched_xtree)

                # How good are the patches from the local XTREE?
                pred_xtree_local, distr_xtree_local = xgboost(validation,
                                                              patched_xtree_local)

                res[proj[:6]]["alves"].append(impact(test, pred_alves))
                res[proj[:6]]["shatw"].append(impact(test, pred_shatw))
                res[proj[:6]]["olive"].append(impact(test, pred_olive))
                res[proj[:6]]["xtree_bellw"].append(impact(test, pred_xtree))
                res[proj[:6]]["xtree_local"].append(
                    impact(test, pred_xtree_local))

                # Not yet...
                # # How good are the patches from the bellwether lessons?
                # pred_fontana, distr_fontana = xgboost(validation, patched_xtree)
                #
                # # res[proj[:6]]["fontana"].append(pred[1])

            yield res


def run_experiment():
    reps = dict()
    import random

    for n in xrange(1):
        for res in transfer_lessons():
            random.seed(n)  # Set a new seed for every run

            if not res.keys()[0] in reps.keys():
                reps.update({res.keys()[0]: res[res.keys()[0]]})
            else:
                reps[res.keys()[0]]["xtree_local"].extend(
                    res[res.keys()[0]]["xtree_local"])
                reps[res.keys()[0]]["xtree_bellw"].extend(
                    res[res.keys()[0]]["xtree_bellw"])
                reps[res.keys()[0]]["alves"].extend(
                    res[res.keys()[0]]["alves"])
                reps[res.keys()[0]]["shatw"].extend(
                    res[res.keys()[0]]["shatw"])
                reps[res.keys()[0]]["olive"].extend(
                    res[res.keys()[0]]["olive"])

    for n, (key, value) in enumerate(reps.iteritems()):
        print(n + 1
              , key
              , np.median(value["xtree_bellw"], axis=0)
              , np.percentile(value["xtree_bellw"], 25, axis=0)
              , np.percentile(value["xtree_bellw"], 75, axis=0)
              , np.median(value["xtree_local"], axis=0)
              , np.percentile(value["xtree_local"], 25, axis=0)
              , np.percentile(value["xtree_local"], 75, axis=0)
              , np.median(value["alves"], axis=0)
              , np.percentile(value["alves"], 25, axis=0)
              , np.percentile(value["alves"], 75, axis=0)
              , np.median(value["shatw"], axis=0)
              , np.percentile(value["shatw"], 25, axis=0)
              , np.percentile(value["shatw"], 75, axis=0)
              , np.median(value["olive"], axis=0)
              , np.percentile(value["olive"], 25, axis=0)
              , np.percentile(value["olive"], 75, axis=0)
              , sep="\t")

    set_trace()


if __name__ == "__main__":
    run_experiment()
