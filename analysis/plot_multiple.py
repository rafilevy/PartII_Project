import argparse

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

df1 = pd.read_csv("/Users/rafilevy/PartII_Project/noisy_data.csv", skiprows=15)
df2 = pd.read_csv("/Users/rafilevy/PartII_Project/results_temp/TEK00000.CSV", skiprows=15)
fig = px.line(df1, y="CH1", x="TIME")
fig.add_trace(go.Line(
    y=df2["CH1"], x=df2["TIME"]
))
fig.show()