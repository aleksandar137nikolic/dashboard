
# Example Dataset -> measuring the environment in a meeting room
# Panel can be used for dashboards as well as interactive apps.

import pandas as pd;
import numpy as np;
import matplotlib.pyplot as plt
import matplotlib as mpl
import panel as pn
from matplotlib.figure import Figure


csv_file = 'https://raw.githubusercontent.com/holoviz/panel/main/examples/assets/occupancy.csv'
data = pd.read_csv(csv_file, parse_dates=['date'], index_col='date')

data.tail()



mpl.use('agg')

def mpl_plot(avg, highlight):
    fig = Figure()
    ax = fig.add_subplot()
    avg.plot(ax=ax)
    if len(highlight): highlight.plot(style='o', ax=ax)
    return fig

def find_outliers(variable='Temperature', window=30, sigma=10, view_fn=mpl_plot):
    avg = data[variable].rolling(window=window).mean()
    residual = data[variable] - avg
    std = residual.rolling(window=window).std()
    outliers = (np.abs(residual) > std * sigma)
    return view_fn(avg, avg[outliers])


pn.extension()

window = pn.widgets.IntSlider(name='window', value=30, start=1, end=60)
sigma = pn.widgets.IntSlider(name='sigma', value=10, start=0, end=20)

interactive = pn.bind(find_outliers, window=window, sigma=sigma)

first_app = pn.Column(window, sigma, interactive)

first_app

first_app.show()

#first_app.servable()