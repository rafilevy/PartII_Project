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

df = pd.DataFrame()
df["n_bytes"] = np.linspace(20, 200, 10)
df["energy"] = np.array([0.028, 0.041, 0.061, 0.068, 0.074, 0.092, 0.105, 0.115, 0.131, 0.137])
fig = px.line(df, x="n_bytes", y="energy")
fig.update_xaxes( title_text="Data sent (B)")
fig.update_yaxes( title_text="Energy consumed (J)")
fig.show()