import pandas as pd
import numpy as np
from sys import argv

def import_trace(path):
    df = pd.read_csv(path, skiprows=15)
    return df

def area_under_graph(df: pd.DataFrame, x_0, x_1):
    dts = df["TIME"].diff()
    ch_1_shifted = df["CH1"].shift()
    df["areas"] = dts * (ch_1_shifted + ((df["CH1"] - ch_1_shifted)/2))
    areas = df[(df["TIME"] >= x_0) & (df["TIME"] <= x_1)]["areas"]
    return np.sum(areas)

if __name__ == "__main__":
    if len(argv) > 1:
        df = import_trace(argv[1])