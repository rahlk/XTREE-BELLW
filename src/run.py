from __future__ import print_function, division

import os
import sys

# Update path
root = os.path.join(os.getcwd().split('src')[0], 'src')
if root not in sys.path:
    sys.path.append(root)

import Misc.logo
import numpy as np
from ipdb import set_trace
from Experiments import Exp2

if __name__ == "__main__":
    reps = dict()
    import random

    for n in xrange(1):
        for res in Exp2.transfer_lessons():
            random.seed(n)  # Set a new seed for every run

            if not res.keys()[0] in reps.keys():
                reps.update({res.keys()[0]: res[res.keys()[0]]})
            else:
                reps[res.keys()[0]]["pd"].extend(res[res.keys()[0]]["pd"])
                reps[res.keys()[0]]["pf"].extend(res[res.keys()[0]]["pf"])
                reps[res.keys()[0]]["local"].extend(
                    res[res.keys()[0]]["local"])
                reps[res.keys()[0]]["bellw"].extend(
                    res[res.keys()[0]]["bellw"])
            # break

    for n, (key, value) in enumerate(reps.iteritems()):
        print(n
              , key
              , np.median(value["pd"], axis=0)
              , np.percentile(value["pd"], 25, axis=0)
              , np.percentile(value["pd"], 75, axis=0)
              , np.median(value["pf"], axis=0)
              , np.percentile(value["pf"], 25, axis=0)
              , np.percentile(value["pf"], 75, axis=0)
              , np.median(value["local"], axis=0)
              , np.percentile(value["local"], 25, axis=0)
              , np.percentile(value["local"], 75, axis=0)
              , np.median(value["bellw"], axis=0)
              , np.percentile(value["bellw"], 25, axis=0)
              , np.percentile(value["bellw"], 75, axis=0)
              , sep="\t")
              # , file=open(os.path.join(root, "plot_data/exp2/data"), "a+"))

    set_trace()
