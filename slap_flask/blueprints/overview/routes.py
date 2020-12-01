from flask import Blueprint, abort

from slap_dj.app.models import Song

overview_bp = Blueprint('overview', __name__, template_folder='templates')


@overview_bp.route('/', defaults={'page': 'index'})
@overview_bp.route('/<page>')
def show(page):
    try:
        Song.objects.all()
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(401)
