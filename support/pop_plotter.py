from pandas import DataFrame
from pandas import options
from plotly.graph_objs import Figure
from plotly import graph_objects as go
import plotly.express as px

from slap_dj.app.init import start_django_lite
start_django_lite()

from slap_dj.app.models import Song

options.plotting.backend = "plotly"


def get_generated_scatter_plot() -> Figure:
    song_list = [
        (f"{song.title} - {song.artist_names}", song.compressibility, song.spotify_popularity, song.word_count)
        for song in Song.objects.all()
    ]
    df = DataFrame(song_list, columns=['Name', 'Compressibility', 'Spotify Popularity', 'Word Count'])
    fig: Figure = px.scatter(df, x='Compressibility', y='Spotify Popularity', custom_data=['Name', 'Word Count'])
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


if __name__ == '__main__':
    get_generated_scatter_plot()
