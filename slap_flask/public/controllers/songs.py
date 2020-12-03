from flask import request, jsonify, abort

from repetition import get_bow_dataframe
from services.genius import tokenize_words
from slap_dj.app.models import Song, Genre
from slap_flask.models.searchers import SongSearcher
from support.popularity_rank import get_word_popularity_index_from_song

DEFAULT_PLOTTER = 'plotly'
INDICATORS = ['youtube_views', 'spotify_streams']


def get_song():
    title = request.args.get('title')
    artist = request.args.get('artist')
    result = SongSearcher.search_one(title=title, artists__name=artist)
    artists = [a.as_dict() for a in result.artists.all()]
    genres = [a.as_dict()['name'] for a in result.genres.all()]
    if result is not None:
        return jsonify({'song_id': result.id,
                        'title': result.title,
                        'artists': artists,
                        'genres': genres,
                        'lyrics': result.lyrics,
                        'metrics': {
                            'compressibility': result.compressibility
                        }})
    else:
        return abort(404)


def get_song_by_id(song_id: str):
    result = Song.objects.get(id=song_id)
    artists = [a.as_dict() for a in result.artists.all()]
    genres = [a.as_dict()['name'] for a in result.genres.all()]
    if result is not None:
        return jsonify({'song_id': result.id,
                        'title': result.title,
                        'artists': artists,
                        'genres': genres,
                        'lyrics': result.lyrics,
                        'metrics': {
                            'compressibility': result.compressibility
                        }})


def get_parameterized_word_popularity_single(song_id: str):
    song = Song.objects.get(id=song_id)
    word_count_weight = request.args.get('word_count_weight', type=float)
    popularity_weight = request.args.get('popularity_weight', type=float)
    popularity_indicator = request.args.get('popularity_indicator', default='youtube_views')
    score = get_word_popularity_index_from_song(song, popularity_indicator, popularity_weight, word_count_weight)
    return jsonify({
        'song_id': song_id,
        'score': score
    })


# TODO: Popularity and Lyrics
def get_song_metrics(song_id: str):
    for_graph = request.args.get('for_graph', type=bool)
    song = Song.objects.get(id=song_id)
    tokenized = tokenize_words(song.lyrics)
    df = get_bow_dataframe(tokenized)
    freq = list(df['freq'])
    words = list(df['word'])
    ranks = list(df['rank'])
    main_dct = {
        'repetition': {
            'bow': {
                'frequencies': freq,
                'words': words,
                'ranks': ranks
            }}
    }
    if for_graph:
        main_dct['chart'] = {
            'library': DEFAULT_PLOTTER,
            'type': 'bar'
        }
    return jsonify(main_dct)


def get_song_genres():
    genres = [{'name': genre.name, 'genre_id': genre.id} for genre in Genre.objects.all()]
    return genres
