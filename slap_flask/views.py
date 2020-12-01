import csv
import io

from flask import Blueprint, render_template, abort, jsonify, make_response, request
from jinja2 import TemplateNotFound

from services.genius import tokenize_words
from services.trends import plot_song_data_google_trends, get_plot_div
from slap_dj.app.models import Song
from slap_flask.models.searchers import SongSearcher
from support.similarity_matrix import get_similarity_matrix_map, all_lyrics

root = Blueprint('view_pages', __name__, template_folder='templates')


@root.route('/', defaults={'page': 'index'})
@root.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(401)


@root.route('/songs')
def get_songs():
    name = request.args.get('name')
    artist = request.args.get('artist')
    songs = Song.objects.all()
    return render_template('songs.html',
                           songs=songs)


@root.route('/song/<song_id>')
def show_song(song_id):
    s = SongSearcher.search_one(id=song_id)
    trends_data, trends_latest = plot_song_data_google_trends(s.title)
    plot_div = get_plot_div(trends_data)
    return render_template('song.html',
                           name=s.title,
                           artists=s.artist_names,
                           lyrics=s.lyrics,
                           song_id=song_id,
                           trends_plot=plot_div,
                           trends_latest=trends_latest)


@root.route('/plot/<song_id>')
def plot(song_id):
    return render_template('index.html', song_id=song_id)


@root.route('/plot/<song_id>/data')
def get_plot_csv(song_id):
    s = SongSearcher.search_one(id=song_id)
    with io.StringIO() as output:
        writer = csv.writer(output
                            , quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["group", "variable", "value"])
        for i in get_similarity_matrix_map(tokenize_words(s.lyrics)):
            writer.writerow(i)
        o = output.getvalue()
    output = make_response(o)
    output.headers["Content-type"] = "text/csv"
    return output


@root.route('/plot/<song_id>/params')
def get_d3_plot_params(song_id):
    s = SongSearcher.search_one(id=song_id)
    return jsonify({'words': tokenize_words(s.lyrics)})


@root.route('/popularity')
def get_popularity():
    return render_template('popularity.html')