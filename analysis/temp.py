# import plotly.express as px
# import pandas as pd
# import numpy as np

# def powerDefault(I_s):
#     return (2.195 + 2.97e-5*I_s)/(13.53 + I_s)

# def powerBatching(N: int, I_s):
#     return (1.1623*(N-1) + 2.195 + N*2.97e-5*I_s)/(13.53 + 6.5*(N-1) + N*I_s)

# df = pd.DataFrame()
# df["I_s"] = np.linspace(20, 600, 580)
# df["power_default"] = powerDefault(df["I_s"])
# for i in range(20, 20, 2):
#     df["power_batch_" + str(i)] = powerBatching(i, df["I_s"])


# y_data = ["power_default"] + ["power_batch_" + str(i) for i in range(2, 20, 2)]
# fig = px.line(df, x="I_s", y=y_data)
# fig.show()

import plotly.express as px
import pandas as pd
import numpy as np

data_write = [(0.015545600000000014, -4.784, -4.528, 0.2560000000000002),
(0.03453439999999999, -3.056, -2.512, 0.544),
(0.05162240000000001, -1.024, -0.208, 0.8160000000000001),
(0.07295360000000001, 1.264, 2.4, 1.136),
(0.08915200000000002, 3.888, 5.28, 1.3920000000000003)]

data_read = [(0.010400000000000008, 2.944, 3.12, 0.17600000000000016),
(0.020403200000000014, 4.608, 4.944, 0.3360000000000003),
(0.030969599999999972, 6.416, 6.928, 0.5119999999999996),
(0.04158719999999993, 8.384, 9.072, 0.6879999999999988),
(0.051152, 10.56, 11.39, 0.8300000000000001)
]

# df = pd.DataFrame()
# df["n_bytes"] = np.array([200,400,600,800,1000])
# df["read"] = [d[0]*3.3 for d in data_read] 
# df["write"] = [d[0]*3.3 for d in data_write] 
# fig = px.line(df, x="n_bytes", y=["read", "write"])
# fig.update_xaxes( title_text="Data sent (B)")
# fig.update_yaxes( title_text="Energy consumed (J)")
# fig.show()
