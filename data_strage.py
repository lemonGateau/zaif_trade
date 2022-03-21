import pandas as pd
from datetime import *


class DataStrage:
    def __init__(self):
        pass

    def load_csv(self, path):
        return pd.read_csv(path, header=0, names=["date", "last"])
