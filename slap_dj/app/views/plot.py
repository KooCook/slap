from pandas import DataFrame, Series
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Song
from app.support.plotter import get_fitted_line_params


class RepetitionPopularityPlotView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    def each_item(self, x):
        if x.name == 'artistinsong__artist__name':
            if len(x.values) > 1:
                return " feat. ".join(x.values[:2])
            return x.values[0]
        if x.name == 'title':
            return x.values[0]
        if isinstance(x, Series):
            if str(x.name).isnumeric():
                if len(x.values) > 1:
                    return " feat. ".join(x.values[:2])
                return x.values[0]
        return x.values[0]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        rep_facet = self.request.query_params.get('rep_facet', 'compressibility')
        pop_facet = self.request.query_params.get('pop_facet', 'spotify_popularity')
        if pop_facet == 'youtube_view':
            pop_facet = 'youtubevideo__view_count'
        df: DataFrame = Song.objects.all().values('id', rep_facet, pop_facet, 'title', 'artistinsong__artist__name').to_dataframe()
        df = df.groupby(by=["id"]).agg(self.each_item)
        df = df.query(f'artistinsong__artist__name.notnull() & {pop_facet}.notnull()')
        df['title-artist'] = df[['title', 'artistinsong__artist__name']].agg(' - '.join, axis=1)
        text_label = 'title-artist'
        x_dat = df[rep_facet]
        y_dat = df[pop_facet]
        x_line, y_line, r_val = get_fitted_line_params(x_dat, y_dat)
        return Response({'data':
                             {
                                 'text': df[text_label], 'x': x_dat, 'y': y_dat,
                                 'type': 'scatter'
                             },
        'line_data': {
            'x': x_line,
            'y': y_line,
            'r_val': r_val
        }})
