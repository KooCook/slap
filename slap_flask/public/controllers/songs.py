from flask import request, jsonify, abort

from slap_flask.models.searchers import SongSearcher


def get_song():
    title = request.args.get('title')
    artist = request.args.get('artist')
    result = SongSearcher.search_one(title=title, artists__name=artist)
    artists = [a.as_dict() for a in result.artists.all()]
    genres = [a.as_dict()['name'] for a in result.genres.all()]
    if result is not None:
        return jsonify({'title': result.title,
                        'artists': artists,
                        'genres': genres,
                        'lyrics': result.lyrics,
                        'metrics': {
                            'compressibility': result.compressibility
                        }})
    else:
        return abort(404)
