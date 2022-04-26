import argparse

import plotly.express as px
import pandas as pd
from sys import argv

parser = argparse.ArgumentParser(description='Plot a graph')
parser.add_argument("path", type=str)
parser.add_argument("--dtick_x", type=float)
parser.add_argument("--dtick_y", type=float)
parser.add_argument("--title", type=str)
parser.add_argument("--x_label", type=str)
parser.add_argument("--y_label", type=str)

args = vars(parser.parse_args())
df = pd.read_csv(args["path"], skiprows=15)
fig = px.line(df, y="CH1", x="TIME")
fig.update_yaxes( title_text=args["y_label"], dtick= args["dtick_y"])
fig.update_xaxes( title_text=args["x_label"], dtick= args["dtick_x"])
fig.show()