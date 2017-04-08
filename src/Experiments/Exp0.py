"""
A lot of talk on XGBoost these days. 
This is how it compares with Random Forest for defect prediction on our data
"""

from __future__ import print_function, division

import os
import sys

# Update path
root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)

import numpy as np
from Data.DefectPrediction import DefectData
from Utils.FileUtil import list2dataframe
from oracle.model import rforest, xgboost
from ExperimentUtils import pred_stats
from pdb import set_trace


def test_oracles(data=None):
    if data is None:
        data = DefectData.get_all_projects()["Apache"]

    for proj, paths in data.iteritems():
        "Make sure we don't test on the bellwether dataset"

        if not proj in paths.bellw:
            res = {
                proj[:6]:
                    {
                        "pd_rf": [],
                        "pf_rf": [],
                        "pd_xg": [],
                        "pf_xg": []
                    }
            }

            pred, pred2, distr, distr2 = [], [], [], []

            validate = list2dataframe(paths.data[:-1])
            test = list2dataframe(paths.data[-1])

            set_trace()

            # How good are the predictions

            pred1, distr1 = rforest(validate, test)
            pred2, distr2 = xgboost(validate, test)

            pred_rf = pred_stats(before=test[test.columns[-1]],
                                 after=pred1,
                                 distr=distr1)
            pred_xg = pred_stats(before=test[test.columns[-1]],
                                 after=pred2,
                                 distr=distr2)

            res[proj[:6]]["pd_rf"].append(pred_rf[0])
            res[proj[:6]]["pf_rf"].append(pred_rf[1])

            res[proj[:6]]["pd_xg"].append(pred_xg[0])
            res[proj[:6]]["pf_xg"].append(pred_xg[1])

            yield res


if __name__ == "__main__":
    reps = dict()
    import random

    for n in xrange(12):
        for res in test_oracles():
            random.seed(n)  # Set a new seed for every run

            print(n, res.keys()[0])
            if not res.keys()[0] in reps.keys():
                reps.update({res.keys()[0]: res[res.keys()[0]]})
            else:
                reps[res.keys()[0]]["pd_rf"].extend(
                    res[res.keys()[0]]["pd_rf"])
                reps[res.keys()[0]]["pf_rf"].extend(
                    res[res.keys()[0]]["pf_rf"])
                reps[res.keys()[0]]["pd_xg"].extend(
                    res[res.keys()[0]]["pd_xg"])
                reps[res.keys()[0]]["pf_xg"].extend(
                    res[res.keys()[0]]["pf_xg"])

    for n, (key, value) in enumerate(reps.iteritems()):
        print(key
              , np.median(value["pd_rf"], axis=0)
              , np.percentile(value["pd_rf"], 25, axis=0)
              , np.percentile(value["pd_rf"], 75, axis=0)
              , np.median(value["pf_rf"], axis=0)
              , np.percentile(value["pf_rf"], 25, axis=0)
              , np.percentile(value["pf_rf"], 75, axis=0)
              , np.median(value["pd_xg"], axis=0)
              , np.percentile(value["pd_xg"], 25, axis=0)
              , np.percentile(value["pd_xg"], 75, axis=0)
              , np.median(value["pf_xg"], axis=0)
              , np.percentile(value["pf_xg"], 25, axis=0)
              , np.percentile(value["pf_xg"], 75, axis=0)
              , sep="\t\t")

    set_trace()
