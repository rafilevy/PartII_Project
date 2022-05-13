import string
import pandas as pd
import numpy as np
from sys import argv

def import_trace(path):
    df = pd.read_csv(path, skiprows=15)
    return df

def find_peak(df: pd.DataFrame, x_0, x_1, threshold_0, threshold_1):
    df_ = df[(df["TIME"] >= x_0) & (df["TIME"] <= x_1)]
    rolling_mean = df_["CH1"].rolling(5).mean().shift()
    peak_x0 = next(iter(np.where((df_["CH1"] - rolling_mean) > threshold_0)[0]), -1)
    if peak_x0 == -1:
        return None
    peak_x0 += df_.index[0]
    y_0 = rolling_mean.loc[peak_x0]
    peak_x1 = next(iter(np.where((np.abs(df_.loc[peak_x0:]["CH1"] - y_0) <= threshold_1) & (np.abs(rolling_mean.shift(-5).loc[peak_x0:] - y_0) <= threshold_1))[0]), -1)
    if peak_x1 == -1:
        return None
    peak_x1 += peak_x0

    return (peak_x0, peak_x1)

def area_under_graph(df: pd.DataFrame, x_0, x_1, x_col=None ):
    if x_col != None:
        df_ = df[(df[x_col] >= x_0) & (df[x_col] <= x_1)]
        x_0 = df_.index[0]
        x_1 = df_.index[-1]
    else:
        df_ = df.loc[x_0: x_1 + 1]
    dts = df_["TIME"].diff()
    ch_1_shifted = df_["CH1"].shift()
    areas = dts * (ch_1_shifted + ((df_["CH1"] - ch_1_shifted)/2))
    time_0 = df_.loc[x_0, "TIME"]
    time_1 = df_.loc[x_1, "TIME"]
    return (np.sum(areas), time_0, time_1, time_1 - time_0)

if __name__ == "__main__":
    if len(argv) > 1:
        df = import_trace(argv[1])