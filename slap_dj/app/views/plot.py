import csv
import io
from itertools import chain

from pandas import DataFrame, Series
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework_csv.renderers import CSVRenderer

from app.support.lyric_metrics import get_lyrics_frequency_df
from app.support.similarity_matrix import get_similarity_matrix_map_v2
from ..model_generator import retrieve_cached_song
from app.support.plotter import get_fitted_line_params

from ..models import Song


class RepetitionPopularityPlotView(APIView):
    """
    """

    def process_each(self, x):
        # if isinstance(x, Series):
        #     if str(x.name).isnumeric():
        #         if len(x.values) > 1:
        #             return " feat. ".join(x.values[:2])
        #         return x.values[0]
        # if x.title == 'artistinsong__artist__name':
        #     if len(x.values) > 1:
        #         return " feat. ".join(x.values[:2])
        #     return x.values[0]
        # if x.title == 'title':
        #     return x.values[0]
        return x.values[0]

    def get(self, request):
        rep_facet = self.request.query_params.get('rep_facet', 'compressibility')
        pop_facet = self.request.query_params.get('pop_facet', 'spotify_popularity')
        if pop_facet == 'youtube_view':
            pop_facet = 'youtubevideo__view_count'
        df: DataFrame = Song.objects.all().values('id', rep_facet, pop_facet, 'title', 'artistinsong__artist__name').to_dataframe()
        df = df.groupby(by=["id"]).agg(self.process_each)
        df = df.query(f'artistinsong__artist__name.notnull() & {pop_facet}.notnull()')
        df['title-artist'] = df[['title', 'artistinsong__artist__name']].agg(' - '.join, axis=1)
        text_label = 'title-artist'
        x_dat = df[rep_facet]
        y_dat = df[pop_facet]
        x_line, y_line, r_squared_val, slope = get_fitted_line_params(x_dat, y_dat)
        return Response({'data':
                             {'text': df[text_label], 'x': x_dat, 'y': y_dat,
                              'type': 'scatter'},
                         'line_data': {
                             'x': x_line, 'y': y_line,
                             'r_val': r_squared_val,
                             'slope': slope
                         }})


class RepetitionMatrixV2Renderer(CSVRenderer):
    header = ['x', 'y', 'word', 'color']


class RepetitionMatrixPlotView(APIView):
    renderer_classes = tuple(chain((RepetitionMatrixV2Renderer,), api_settings.DEFAULT_RENDERER_CLASSES))

    def get(self, request, song_id: str):
        s = retrieve_cached_song(pk=song_id)
        content = [{
            'x': row[0],
            'y': row[1],
            'word': row[2],
            'color': row[3],
        } for row in get_similarity_matrix_map_v2(s.words)]
        return Response(content)


class SongWordFrequencyPlotView(APIView):
    def get(self, request, song_id: str):
        s = retrieve_cached_song(pk=song_id)
        df = get_lyrics_frequency_df(s.lyrics)
        content = {
            'x': df['words'],
            'y': df['count']
        }
        return Response(content)
