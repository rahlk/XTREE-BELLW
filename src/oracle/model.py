from __future__ import division

import os
import sys
from pdb import set_trace
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from Utils.FileUtil import list2dataframe
from sklearn.metrics import roc_curve, roc_auc_score
from smote import SMOTE
from sklearn.model_selection import train_test_split

root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)


def getTunings(fname):
    raw = pd.read_csv(root + '/old/tunings.csv').transpose().values.tolist()
    formatd = pd.DataFrame(raw[1:], columns=raw[0])
    try:
        return formatd[fname].values.tolist()
    except KeyError:
        return None


def rforest(train, target):
    clf = RandomForestClassifier(n_estimators=100, random_state=1)
    try:
        source = list2dataframe(train)
    except IOError:
        source = train

    source = SMOTE(source)

    source.loc[source[source.columns[-1]] == 0, source.columns[-1]] = False
    features = source.columns[:-1]
    klass = list(source[source.columns[-1]])
    clf.fit(source[features], klass)
    preds = clf.predict(target[target.columns[:-1]])
    distr = clf.predict_proba(target[target.columns[:-1]])[:, 1]

    return preds, distr


def _test_model():
    pass


if __name__ == '__main__':
    _test_model()
