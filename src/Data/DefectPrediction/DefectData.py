import os
import sys

root = os.path.join("/".join(os.getcwd().split('/')[:-1]))
if root not in sys.path:
    sys.path.append(root)
from glob import glob
from ipdb import set_trace

class _Data:
    """Hold training and testing data"""

    def __init__(self, dataName='ant', type='jur'):
        if type == 'jur':
            dir = os.path.join(root, "Data/DefectPrediction/Jureczko")
            bell = 'lucene'
        elif type == 'nasa':
            dir = os.path.join(root, "Data/DefectPrediction/mccabe")
            bell = 'mc'
        elif type == 'aeeem':
            dir = os.path.join(root, "Data/DefectPrediction/AEEEM")
            bell = 'LC'
        elif type == "relink":
            bell = 'Safe'
            dir = os.path.join(root, "Data/DefectPrediction/Relink")

        self.data = glob(os.path.join(dir, dataName, "*.csv"))
        self.bellw = bell

class NASA:
    "NASA"

    def __init__(self):
        self.projects = {}
        for file in ["cm", "jm", "kc", "mc", "mw"]:
            self.projects.update({file: _Data(dataName=file, type='nasa')})


class Jureczko:
    "Apache"

    def __init__(self):
        self.projects = {}
        for file in ['ant', 'camel', 'ivy', 'jedit', 'log4j',
                     'lucene', 'poi', 'velocity', 'xalan', 'xerces']:
            self.projects.update({file: _Data(dataName=file, type='jur')})


class AEEEM:
    "AEEEM"

    def __init__(self):
        self.projects = {}
        for file in ["EQ", "JDT", "LC", "ML", "PDE"]:
            self.projects.update({file: _Data(dataName=file, type='aeeem')})


class ReLink:
    "RELINK"

    def __init__(self):
        self.projects = {}
        for file in ["Apache", "Safe", "Zxing"]:
            self.projects.update({file: _Data(dataName=file, type='relink')})


def get_all_projects():
    all = dict()
    for community in [Jureczko, AEEEM, ReLink, NASA]:
        all.update({community.__doc__: community().projects})
    return all


def _test():
    data = NASA()


if __name__ == "__main__":
    _test()
