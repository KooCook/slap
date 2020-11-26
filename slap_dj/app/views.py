from django.shortcuts import render

# Create your views here.
from plotly.offline import plot

import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json


def create_plot():
    N = 40
    x = np.linspace(0, 1, N)
    y = np.random.randn(N)
    df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe
    data = [
        go.Bar(
            x=df['x'], # assign x as the dataframe column 'x'
            y=df['y']
        )
    ]
   # graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return data # graphJSON


def index(request):
    plot_div = plot(create_plot(), output_type='div', include_plotlyjs=False)
    context = {'plot': plot_div}
    return render(request, 'plot.html', context)
