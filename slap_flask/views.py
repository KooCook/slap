import csv
import io

from django.core.paginator import Paginator
from flask import Blueprint, render_template, abort, jsonify, make_response, request
from jinja2 import TemplateNotFound

from services.genius import tokenize_words
from services.trends import get_rendered_plot
from slap_dj.app.models import Song
from slap_flask.models.searchers import SongSearcher
from support.lyric_metrics import plot_lyrics_frequency
from support.pop_plotter import get_generated_scatter_plot
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
    songs = Song.objects.all()
    paginator = Paginator(songs, 25)
    # page = request.args.get(get_page_parameter(), type=int, default=1)
    # pagination = Pagination(page=page, total=Song.objects.count())
    page_number = request.args.get('page')
    page_obj = paginator.get_page(page_number)
    return render_template('songs.html', songs=songs, page_obj=page_obj)


@root.route('/song/<song_id>')
def show_song(song_id):
    s = SongSearcher.search_one(id=song_id)
    fig = plot_lyrics_frequency(s.lyrics)
    plot_div = get_rendered_plot(fig)
    return render_template('song.html',
                           name=s.title,
                           artists=s.artist_names,
                           lyrics=s.lyrics,
                           song_id=song_id,
                           word_freq_plot=plot_div)


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
    return render_template('popularity.html', compressibility_vs_pop=get_rendered_plot(get_generated_scatter_plot()))


@root.route('/repetition')
def get_repetition():
    return render_template('repetition.html')
