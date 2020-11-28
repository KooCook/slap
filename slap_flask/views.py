from flask import Blueprint, render_template, abort, jsonify, make_response
from jinja2 import TemplateNotFound
from support.similarity_matrix import get_similarity_matrix_map, all_lyrics

root = Blueprint('view_pages', __name__, template_folder='templates')


@root.route('/', defaults={'page': 'index'})
@root.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(401)


@root.route('/plot')
def plot():
    return render_template('index.html')


@root.route('/plot/data')
def get_plot_csv():
    import csv
    import io
    with io.StringIO() as output:
        spamwriter = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["group", "variable", "value"])
        for i in get_similarity_matrix_map(all_lyrics):
            spamwriter.writerow(i)
        o = output.getvalue()
    output = make_response(o)
    output.headers["Content-type"] = "text/csv"
    return output


@root.route('/plot/params')
def get_d3_plot_params():
    return jsonify({'words': all_lyrics})
