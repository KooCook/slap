import operator
from functools import reduce
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import options
from scipy import stats

import plotly.express as px
from django.core.exceptions import ObjectDoesNotExist
from nltk import collections
from plotly import graph_objs as go
from plotly.subplots import make_subplots
from services.genius import tokenize_words, tokenize_words_simple
from slap_dj.app.init import start_django_lite
from slap_dj.app.models import Genre, Song

start_django_lite()

options.plotting.backend = "plotly"


def do_regression_using_scientific(x, y) -> None:
    # x: pd.Series
    # y: pd.Series
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    print("R-squared: %f" % r_value ** 2)
    print("slope: %f    intercept: %f" % (slope, intercept))
    plt.plot(x, y, 'o', label='original data')
    plt.plot(x, intercept + slope * x, 'r', label='fitted line')
    plt.legend()
    plt.show()


def add_fitted_line_trace(fig: go.Figure, xdata, ydata,
                          name: str = 'fitted line',
                          line_tick: float = 0.01) -> None:
    """ Fits data using linear regression and add trace to plot. """
    # xdata: pd.Series
    # ydata: pd.Series
    slope, intercept, r_value, p_value, std_err = stats.linregress(xdata, ydata)
    p = np.arange(xdata.min(), xdata.max(), line_tick)
    fig.add_trace(
        # TODO: Use non-depreciated line graph
        go.Line(x=p, y=intercept + slope * p, name=name, mode='lines')
    )
    fig.update_traces(
        selector={'name': name},
        hovertemplate="<br>".join([
            "x: %{x}",
            "y: %{y}",
            f"slope: {slope}",
            f"R-squared: {r_value ** 2}",
        ])
    )


def get_scatter_plt(df: pd.DataFrame, title_text: str = None, show_regression: bool = False) -> go.Figure:
    """Returns a scatter plot from dataframe.

    Args:
        df: DataFrame containing data for the graph.
            The first column is used as the 'name' (shown when hovered).
            The second column is used as the x value.
            The third column is used as the y value.
            The rest are appended to the hovertext.
        title_text: Title of the graph, if any.
        show_regression: Flag to show or not show regression line.
    """
    it = df.items()
    name, names = next(it)
    x, xdata = next(it)
    y, ydata = next(it)
    custom_data = [name]
    hoveritems = ["%{customdata[0]}", f"{x}: %{{x}}", f"{y}: %{{y}}"]
    for i, (k, v) in enumerate(it):
        custom_data.append(k)
        hoveritems.append(f"{k}: %{{customdata[{i+1}]}}")
    hovertemplate = "<br>".join(hoveritems)

    fig: go.Figure = px.scatter(df, x=x, y=y, custom_data=custom_data)
    fig.update_traces(
        selector='scatter',
        hovertemplate=hovertemplate,
    )
    if show_regression:
        add_fitted_line_trace(fig, xdata, ydata)
    if title_text is not None:
        fig.update_layout(title_text=title_text)
    return fig


def get_comp_vs_yt_view_plt() -> go.Figure:
    song_list = []
    for song in Song.objects.all():
        try:
            song_list.append((
                f"{song.title} - {song.artist_names}",
                song.compressibility,
                song.youtubevideo.view_count,
                song.word_count,
            ))
        except ObjectDoesNotExist as e:
            assert e.args[0] == 'Song has no youtubevideo.'

    df = pd.DataFrame(song_list, columns=['Name', 'Compressibility', 'YouTube View', 'Word Count'])
    fig = get_scatter_plt(df, title_text='Compressibility vs. YouTube View', show_regression=True)
    return fig


def get_comp_vs_spo_pop_plot() -> go.Figure:
    song_list = [
        (f"{song.title} - {song.artist_names}", song.compressibility, song.spotify_popularity, song.word_count)
        for song in Song.objects.all()
    ]

    df = pd.DataFrame(song_list, columns=['Name', 'Compressibility', 'Spotify Popularity Index', 'Word Count'])
    fig = get_scatter_plt(df, title_text='Compressibility vs. Spotify Popularity Index', show_regression=True)
    # fig.add_trace(
    #     go.Scatter(x=df['Compressibility'], y=df['Spotify Popularity'], text="Name", mode='markers'),
    #     secondary_y=False,
    # )
    # fig.update_traces(textposition='top center', textinfo = "label")

    # fig.add_trace(
    #     go.Scatter(x=df['Spotify Popularity'], y=df['Name'], name="Spotify Popularity", mode='markers'),
    #     # secondary_y=True,
    # )
    # fig.update_xaxes(showticklabels=False)
    # fig.show()
    return fig


def get_generated_histogram_plot_genre(genre: str = "r&b"):
    songs_in_genre: List[Song] = reduce(operator.add, [list(g.song_set.all()) for g in Genre.objects.filter(name=genre)], [])
    q = [song.spotify_popularity for song in songs_in_genre]
    df = pd.DataFrame(q, columns=['Spotify Popularity Index'])
    fig = px.bar(df, x='Title', y='Spotify Popularity Index',
                 title=f"Popularity Scores of {genre.title()} songs")
    fig.update_xaxes(showticklabels=False)
    fig.show()


def get_generated_title_occurrence(limit=20) -> go.Figure:
    o = []
    for s in Song.objects.all().order_by('spotify_popularity'):
        try:
            words = tokenize_words(s.lyrics)
            title_words = tokenize_words_simple(s.title)
            exact_occurrences = (word for word in words if s.title in word)
            part_of_occurrences = (word for word in words if word in title_words)
            counts = collections.Counter(exact_occurrences)
            exact_most_common = counts.most_common(limit)
            exact_intermediate = list(b[1] + a[1] for a, b in zip(exact_most_common, exact_most_common[1:]))
            exact_count = reduce(operator.add, exact_intermediate) if len(exact_intermediate) > 0 else 0

            counts = collections.Counter(part_of_occurrences)
            part_of_most_common = counts.most_common(limit)
            part_of_intermediate = list(b[1] + a[1] for a, b in zip(part_of_most_common, part_of_most_common[1:]))
            part_of_count = reduce(operator.add, part_of_intermediate) if len(part_of_intermediate) > 0 else 0
            count = exact_count + part_of_count
            if count > 0:
                o.append((s.title, count, s.spotify_popularity))
        except TypeError:
            continue
    df = pd.DataFrame(o, columns=['Title', 'Word Title Count', 'Spotify Popularity'])
    fig: go.Figure = make_subplots()
    fig.add_trace(go.Scatter(x=df['Word Title Count'], y=df['Spotify Popularity'], mode='markers', name="Exact match"))
    # fig.add_trace(go.Scatter(x=df['Partial Count'], y=df['Spotify Popularity'], text="Name", mode='markers', name="Partial match"))
    fig.update_layout(
        title_text='Title occurrences in lyrics vs. Spotify Popularity Index'
    )
    fig.update_xaxes(title_text='Title occurrences')
    fig.update_yaxes(title_text='Spotify Popularity')
    add_fitted_line_trace(fig, df['Word Title Count'], df['Spotify Popularity'])
    # fig.show()
    return fig


# def get_genre_eng_words()
if __name__ == '__main__':
    # get_generated_scatter_plot()
    get_generated_title_occurrence()
