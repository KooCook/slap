from typing import List

import pandas as pd
from pytrends.request import TrendReq
import plotly.graph_objs as go
from plotly.offline import plot


def retrieve_aggregate_song(song_name: str, mode: str = 'sum') -> pd.DataFrame:
    pytrend = TrendReq(tz=360)
    pytrend.build_payload(
        kw_list=[song_name],
        cat=35)
    df = pytrend.interest_over_time()
    df = df.sort_values(by=song_name)

    df = df.groupby([pd.DatetimeIndex(df.index.date).to_period("Y")]) \
        .agg({song_name: [mode]})
    df = pd.DataFrame({'x': df.index.year, 'y': df[song_name, mode]})
    return df


def plot_song_data_google_trends(song_name: str, mode: str = 'sum') -> go.Figure:
    df = retrieve_aggregate_song(song_name, mode)
    return go.Figure(data=[go.Scatter(x=df['x'], y=df['y'])],
                     layout=go.Layout(title=go.layout.Title(text=f'\"{song_name}\" Keyword Trends - Total Scores')))


def get_plot_div(figure: go.Figure) -> str:
    return plot(figure, output_type='div', include_plotlyjs=False)
# print(df['x'])
# print(df['y'])
# fig = go.Figure(
#     data=[go.Bar(x=[1, 2, 3], y=[1, 3, 2])],
#
# )