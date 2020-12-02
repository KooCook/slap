import numpy as np
import pandas
from django.core.exceptions import ObjectDoesNotExist
from scipy import special

from slap_dj.app.init import start_django_lite

start_django_lite()

from slap_dj.app.models import Song


def popularity_indicator(view_count: int):
    return special.expit((np.log10(view_count) - 5.2) / 0.3)


def get_song_visibility(p_weight: float, view_count: int):
    return p_weight * popularity_indicator(view_count)


def get_song_weighted_count(c_weight: float, song: Song):
    return c_weight * song.word_count


if __name__ == '__main__':
    songs = list(Song.objects.order_by('-youtubevideo__view_count'))
    popularity_indices = []
    for s in songs:
        try:
            y = get_song_visibility(7, s.youtubevideo.view_count) + get_song_weighted_count(3, s)
            popularity_indices.append((s.identifier, y))
        except ObjectDoesNotExist:
            pass
    df = pandas.DataFrame(popularity_indices, columns=['Title-Artist', 'Popularity Rank'])
    print(df)
