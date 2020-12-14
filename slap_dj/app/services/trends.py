"""
Service: Google Trends
via pytrends
"""
from datetime import datetime
from typing import Tuple

import pandas as pd

import plotly.graph_objs as go
from plotly.offline import plot

from pytrends.request import TrendReq


def retrieve_aggregate_song(song_name: str, mode: str = 'sum') -> Tuple[pd.DataFrame, datetime]:
    pytrend = TrendReq(tz=360)
    pytrend.build_payload(
        kw_list=[song_name],
        cat=35)
    df = pytrend.interest_over_time()
    df = df.sort_values(by=song_name)
    latest = df.sort_index().index.values[-1]
    df = df.groupby(
        [pd.DatetimeIndex(df.index.date).to_period("Y")]
    ).agg({song_name: [mode]})
    df = pd.DataFrame({'x': df.index.year, 'y': df[song_name, mode]})
    return df, datetime.utcfromtimestamp(latest.astype('O')/1e9)


def plot_song_data_google_trends(song_name: str, mode: str = 'sum') -> Tuple[go.Figure, datetime]:
    df, latest = retrieve_aggregate_song(song_name, mode)
    return go.Figure(
        data=[go.Scatter(x=df['x'], y=df['y'])],
        layout=go.Layout(
            title=go.layout.Title(text=f'\"{song_name}\" Keyword Trends - Cumulative Scores by year')
        )), latest


def get_rendered_plot(figure: go.Figure) -> str:
    return plot(figure, output_type='div', include_plotlyjs=False)
