import pandas
from dirs import ROOT_DIR

import plotly.express as px

from plotly.offline import plot

d = pandas.read_csv(ROOT_DIR / "data/billboard/year_end.csv")
q = d.query("chart == 'hot-100-songs'")
r = q.assign(freq=q.apply(lambda x: q.artist.value_counts().to_dict()[x.artist], axis=1))\
    .sort_values(by=['freq', 'artist'], ascending=[False, True])\
    .drop_duplicates(subset=['artist']).loc[:, ['artist', 'freq']].iloc[:10]
    # .groupby(['artist']).count().sort_values(by=['freq', 'artist'], ascending=[False, True])
print(r.columns)
fig = px.bar(r, x='artist', y='freq')
fig.show()
print(r)
