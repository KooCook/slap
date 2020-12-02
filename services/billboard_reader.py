from typing import List

import pandas

from dirs import ROOT_DIR
from slap_dj.app.models import BillboardYearEndEntry
from slap_flask.models.searchers import SongSearcher
from support.models import SongModel


def read_billboard_yearly() -> List[SongModel]:
    d = pandas.read_csv(ROOT_DIR / "data/billboard/year_end.csv")
    q = d.query("chart == 'hot-100-songs'")
    s = q.loc[:, ['year', 'artist', 'title', 'rank', 'chart', 'image']]
    r = q.assign(freq=q.apply(lambda x: q.artist.value_counts().to_dict()[x.artist], axis=1))\
        .sort_values(by=['freq', 'artist'], ascending=[False, True])\
        .drop_duplicates(subset=['artist']).loc[:, ['artist', 'freq']].iloc[:10]

    dct = s.to_dict('index')
    ms = []
    for ele in list(dct.items()):
        fields = ele[1]
        try:
            s = SongSearcher.search_one(title=fields['title'], artists__name=fields['artist'])
            if s:
                BillboardYearEndEntry.from_dict(fields, s).save()
        except Exception as e:
            print(e)
            pass
        print(fields['year'], fields['title'])
    return ms
