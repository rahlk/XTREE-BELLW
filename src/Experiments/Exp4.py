"""
The one that determines the magnitude of changes for each learner.
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

from pandas import DataFrame
from oracle.model import rforest, xgboost
from Utils.ExperimentUtils import deltas
from Utils.StatsUtils.CrossVal import CrossValidation


def changes(data=None):
    if data is None:
        data = DefectData.get_all_projects()["Apache"]

    for proj, paths in data.iteritems():
        "Make sure we don't test on the bellwether dataset"

        if not proj in paths.bellw:
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
                                                                 ways=2):
                orig = DataFrame([test.iloc[n].values.tolist() for n in
                                  xrange(test.shape[0]) if
                                  test.iloc[n][-1] > 0], columns=test.columns)

                patched_alves = alves(train_bellw, test)
                patched_shatw = shatnawi(train_bellw, test)
                patched_olive = oliveira(train_bellw, test)
                patched_xtree = xtree(train_bellw, test_local)
                patched_xtree_local = xtree(train_local, test_local)

                # How good are the patches from local lessons?
                res[proj[:6]]["alves"].append(deltas(orig, patched_alves))
                res[proj[:6]]["olive"].append(deltas(orig, patched_olive))
                res[proj[:6]]["shatw"].append(deltas(orig, patched_shatw))
                res[proj[:6]]["xtree_bellw"].append(
                    deltas(orig, patched_xtree))
                res[proj[:6]]["xtree_local"].append(
                    deltas(orig, patched_xtree_local))

            yield res


if __name__ == "__main__":
    data = DefectData.get_all_projects()["Apache"]
    metrics = list2dataframe(data["ant"].data[-1]).columns
    for res in changes(data):
        for key, value in res.iteritems():
            print(key)
            for n, (attr, xtree_local, xtree_bellw, Olive, Alves, Shatw) in \
                    enumerate(
                        zip(metrics,
                            np.median(value["xtree_local"], axis=0),
                            np.median(value["xtree_bellw"], axis=0),
                            np.median(value["olive"], axis=0),
                            np.median(value["alves"], axis=0),
                            np.median(value["shatw"], axis=0))):
                print(n, attr[1:], int(xtree_local), int(xtree_bellw), int(Olive), int(Alves), int(Shatw), sep="\t")

    set_trace()
