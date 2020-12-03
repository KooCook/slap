import operator
from functools import reduce

import numpy as np
import pandas as pd
from pandas import DataFrame, options
from scipy import stats

import plotly.express as px
from nltk import collections
from plotly import graph_objs as go
from plotly.graph_objs import Figure
from plotly.subplots import make_subplots

from services.genius import tokenize_words, tokenize_words_simple
from slap_dj.app.init import start_django_lite
from slap_dj.app.models import Genre, Song

start_django_lite()


options.plotting.backend = "plotly"


def add_fitted_line_trace(fig: Figure, x, y) -> None:
    """ Fits data using linear regression and add trace to plot. """
    # x: pd.Series
    # y: pd.Series
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    # print("R-squared: %f" % r_value ** 2)
    # print("slope: %f    intercept: %f" % (slope, intercept))
    # plt.plot(x, y, 'o', label='original data')
    # plt.plot(x, intercept + slope * x, 'r', label='fitted line')
    # plt.legend()
    # plt.show()

    p = np.arange(x.min(), x.max(), 0.01)
    LINE_NAME = 'fitted line'
    fig.add_trace(
        go.Line(x=p, y=intercept + slope * p, name=LINE_NAME, mode='lines')
    )
    fig.update_traces(
        selector={'name': LINE_NAME},
        hovertemplate="<br>".join([
            "x: %{x}",
            "y: %{y}",
            f"slope: {slope}",
            f"R-squared: {r_value**2}",
        ])
    )


def get_comp_vs_spo_pop_plot() -> Figure:
    song_list = [
        (f"{song.title} - {song.artist_names}", song.compressibility, song.spotify_popularity, song.word_count)
        for song in Song.objects.all()
    ]
    df = pd.DataFrame(song_list, columns=['Name', 'Compressibility', 'Spotify Popularity', 'Word Count'])
    fig: Figure = px.scatter(df,
                             x='Compressibility', y='Spotify Popularity',
                             custom_data=['Name', 'Word Count'],
                             )
    fig.update_traces(
        hovertemplate="<br>".join([
            "%{customdata[0]}",
            "Compressibility: %{x}",
            "Spotify Popularity Index: %{y}",
            "Word Count: %{customdata[1]}",
        ])
    )
    fig.update_layout(
        title_text='Compressibility vs. Spotify Popularity Index'
    )

    add_fitted_line_trace(fig, df.get('Compressibility'), df.get('Spotify Popularity'))

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
    q = [x.spotify_popularity
         for x in reduce(lambda a, b: a+b, [list(g.song_set.all())
                                            for g in Genre.objects.filter(name=genre)], [])]
    df = DataFrame(q, columns=['Spotify Popularity Index'])
    fig = px.bar(df, x='Title', y='Spotify Popularity Index',
                 title=f"Popularity Scores of {genre.title()} songs")
    fig.update_xaxes(showticklabels=False)
    fig.show()


def get_generated_title_occurrence(limit=20) -> Figure:
    o = []
    for s in Song.objects.all().order_by('spotify_popularity'):
        try:
            words = tokenize_words(s.lyrics)
            title_words = tokenize_words_simple(s.title)
            exact_occurrences = [word for word in words if s.title in word]
            part_of_occurrences = [word for word in words if word in title_words]
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
    df = DataFrame(o, columns=['Title', 'Word Title Count', 'Spotify Popularity'])
    fig: Figure = make_subplots()
    fig.add_trace(go.Scatter(x=df['Word Title Count'], y=df['Spotify Popularity'], mode='markers', name="Exact match"))
   #  fig.add_trace(go.Scatter(x=df['Partial Count'], y=df['Spotify Popularity'], text="Name", mode='markers', name="Partial match"))
    fig.update_layout(
        title_text='Title occurrences in lyrics vs. Spotify Popularity Index'
    )
    fig.update_xaxes(title_text='Title occurrences')
    fig.update_yaxes(title_text='Spotify Popularity')
    # fig.show()
    return fig


# def get_genre_eng_words()
if __name__ == '__main__':
    # get_generated_scatter_plot()
    get_generated_title_occurrence()
