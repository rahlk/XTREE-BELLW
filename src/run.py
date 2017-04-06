from __future__ import print_function, division

import os
import sys

# Update path
root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)

from pdb import set_trace
import tools.pyC45 as pyC45
from Data.DefectPrediction import DefectData
from Utils.FileUtil import list2dataframe
from XTREE import XTREE
from oracle.model import rforest
from tools.stats.abcd import abcd
from sklearn.model_selection import train_test_split
import numpy as np


def impact(test, pred):
    actuals = test[test.columns[-1]]
    gain = round(100 - 100 * (sum(actuals) / sum(pred)), 2)

    # print("{}\t{}\t{}".format(np.median(gain)
    #                           , np.percentile(gain, 25)
    #                           , np.percentile(gain, 75)))

    # return [np.median(gain), np.percentile(gain, 25), np.percentile(gain, 75)]
    return gain


def pred_stats(before, after, distr):
    pd, pf = abcd(before, after, distr)[:2]
    return round(pd, 2), round(pf, 2)


def transfer_lessons(n_reps=10):
    data = DefectData.get_all_projects()["Apache"]
    # print("Name\tPd(Med)\tPf\tImprovement")
    for proj, paths in data.iteritems():
        if not proj in paths.bellw:
            res = {proj[:6]: []}
            "If training data doesn't exist, create it."
            pred, pred2, distr, distr2 = [], [], [], []

            if not "train" in locals():
                train = list2dataframe(data[paths.bellw].data)

            test, validation = train_test_split(list2dataframe(paths.data),
                                                test_size=0.8)
            # test = list2dataframe(paths.data[-1])
            # validation = list2dataframe(paths.data[:-1])
            patched = XTREE.execute(train, test)
            a, b = rforest(validation, patched)  # How good are the patches
            aa, bb = rforest(validation, test)  # How good are the predcitions
            pred.append(a)
            pred2.append(aa)
            distr.append(b)
            distr2.append(bb)

            res[proj[:6]].extend(pred_stats(before=test[test.columns[-1]],
                                            after=pred2,
                                            distr=distr2))

            res[proj[:6]].append(impact(test, pred))
            return res


def transfer_lessons3():
    data = DefectData.get_all_projects()["Apache"]
    for proj, paths in data.iteritems():
        if not proj in paths.bellw:
            res = {proj[:6]: []}
            "If training data doesn't exist, create it."
            pred, pred2, distr, distr2 = [], [], [], []

            if not "train" in locals():
                train = list2dataframe(data[paths.bellw].data)

            test, validation = train_test_split(list2dataframe(paths.data),
                                                test_size=0.8)
            # test = list2dataframe(paths.data[-1])
            # validation = list2dataframe(paths.data[:-1])
            patched = XTREE.execute(train, test)
            a, b = rforest(train, patched)  # How good are the patches
            aa, bb = rforest(train, test)  # How good are the predcitions
            pred.append(a)
            pred2.append(aa)
            distr.append(b)
            distr2.append(bb)
            res[proj[:6]].extend(pred_stats(before=test[test.columns[-1]],
                                            after=pred2,
                                            distr=distr2))

            res[proj[:6]].extend(impact(test, pred))
            yield res


def transfer_lessons4():
    data = DefectData.get_all_projects()["Apache"]
    for proj, paths in data.iteritems():
        if not proj in paths.bellw:
            res = {proj[:6]: []}
            "If training data doesn't exist, create it."
            pred, pred2, distr, distr2 = [], [], [], []

            if not "train_bellw" in locals():
                train_bellw = list2dataframe(data[paths.bellw].data)

            train_local = list2dataframe(paths.data[:-1])
            test = list2dataframe(paths.data[-1])

            patched_local = XTREE.execute(train_local, test)
            patched_bellw = XTREE.execute(train_bellw, test)

            pred, distr = rforest(train_bellw,
                                  patched_local)  # How good are the patches
            pred2, distr2 = rforest(train_bellw,
                                    patched_bellw)  # How good are the predcitions
            pred3, distr3 = rforest(train_bellw,
                                    test)  # How good are the predcitions

            res[proj[:6]].extend(pred_stats(before=test[test.columns[-1]],
                                            after=pred3,
                                            distr=distr3))

            res[proj[:6]].append(impact(test, pred))
            res[proj[:6]].append(impact(test, pred2))
            yield res


def transfer_lessons2(n_reps=1):
    data = DefectData.get_all_projects()["Apache"]
    print("Name\tPd\tPf\tImprovement")
    for proj, paths in data.iteritems():
        if not proj in paths.bellw:
            print(proj[:4], end="\t")
            "If training data doesn't exist, create it."

            train, validation = train_test_split(list2dataframe(paths.data),
                                                 test_size=0.8)
            test = paths.data[-1]
            validation = paths.data[:-1]
            patched = XTREE.execute(train, test)
            test = list2dataframe(test)
            pred, distr = rforest(validation,
                                  patched)  # How good are the patches
            pred2, distr2 = rforest(validation,
                                    test)  # How good are the predcitions

            pred_stats(before=test[test.columns[-1]],
                       after=pred2,
                       distr=distr2)

            impact(test, pred)
            # set_trace()


if __name__ == "__main__":
    reps = dict()
    import random

    for n in xrange(10):
        for res in transfer_lessons4():
            # print(res.keys()[0])
            random.seed(n)
            if res.keys()[0] in reps.keys():
                reps[res.keys()[0]].append(res[res.keys()[0]])
            else:
                reps.update({res.keys()[0]: [res[res.keys()[0]]]})

    for key, value in reps.iteritems():
        print(key
              , "\t".join([str(x) for x in np.median(value, axis=0)])
              , "\t".join([str(x) for x in np.percentile(value, 25, axis=0)])
              , "\t".join([str(x) for x in np.percentile(value, 75, axis=0)])
              , sep="\t")
