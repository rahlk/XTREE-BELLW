from __future__ import print_function, division

from ipdb import set_trace

import pandas as pd
from sklearn.model_selection import StratifiedKFold


class CrossValidation:
    def __init__(self):
        pass

    @classmethod
    def split(cls, dframe, ways=5):
        col = dframe.columns
        X = dframe
        y = dframe[dframe.columns[-1]]
        skf = StratifiedKFold(n_splits=ways, shuffle=True)
        for train_idx, test_idx in skf.split(X, y):
            yield pd.DataFrame(X.values[train_idx], columns=col), \
                  pd.DataFrame(X.values[test_idx], columns=col)
