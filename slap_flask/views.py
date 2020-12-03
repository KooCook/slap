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
from support.pop_plotter import get_comp_vs_spo_pop_plot, get_generated_title_occurrence
from support.similarity_matrix import get_similarity_matrix_map, get_similarity_matrix_map_v2

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
    page_number = request.args.get('page')
    page_obj = paginator.get_page(page_number)
    return render_template('songs.html', songs=songs, page_obj=page_obj)


@root.route('/song/<song_id>')
def show_song(song_id):
    s = SongSearcher.search_one(pk=song_id)
    fig = plot_lyrics_frequency(s.lyrics)
    plot_div = get_rendered_plot(fig)
    return render_template('song.html',
                           name=s.title,
                           artists=s.artist_names,
                           lyrics=s.lyrics,
                           song_id=song_id,
                           word_count=len(tokenize_words(s.lyrics)),
                           word_freq_plot=plot_div)


@root.route('/plot/<song_id>')
def plot(song_id):
    return render_template('index.html', song_id=song_id)


@root.route('/plot/<song_id>/data')
def get_plot_csv(song_id):
    version = 'v2'
    s = SongSearcher.search_one(pk=song_id)
    with io.StringIO() as output:
        writer = csv.writer(output
                            , quoting=csv.QUOTE_MINIMAL)
        if version == 'v1':
            writer.writerow(["group", "variable", "value"]) # v1
        else:
            writer.writerow(["x", "y", "word", "color"]) # v2
        if version == 'v1':
            for i in get_similarity_matrix_map(tokenize_words(s.lyrics)):
                writer.writerow(i)
        else:
            for i in get_similarity_matrix_map_v2(tokenize_words(s.lyrics)):
                writer.writerow(i)
        o = output.getvalue()
    output = make_response(o)
    output.headers["Content-type"] = "text/csv"
    return output


@root.route('/plot/<song_id>/params')
def get_d3_plot_params(song_id):
    s = SongSearcher.search_one(pk=song_id)
    return jsonify({'words': tokenize_words(s.lyrics)})


@root.route('/overview')
def get_overview_page():
    return render_template('overview.html',
                           compressibility_vs_pop=get_rendered_plot(get_comp_vs_spo_pop_plot()),
                           graph2=get_rendered_plot(get_generated_title_occurrence()),
                           markdown_content='',
                           )
