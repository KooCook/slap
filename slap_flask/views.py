from flask import Blueprint, render_template, abort, jsonify, make_response, request
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


@root.route('/get_song')
def get_song():
    name = request.args.get('name')
    artist = request.args.get('artist')
    # p = Song.query.filter_by(name=name, artist=artist).first()


@root.route('/ac1')
def test_view_block():
    return render_template('ac1.html')


@root.route('/song/<song_id>')
def show_song(song_id):
    lyrics = """
    [Intro]
    Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
    Caught in a bad romance
    Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
    Caught in a bad romance
    Ra-ra-ah-ah-ah
    Roma Roma-ma
    Gaga, "Ooh la-la"
    Want your bad romance
    Ra-ra-ah-ah-ah
    Roma, Roma-ma
    Gaga, "Ooh la-la"
    Want your bad romance
    
    [Verse 1]
    I want your ugly, I want your disease
    I want your everything as long as it’s free
    I want your love
    Love, love, love, I want your love, oh, ey
    I want your drama, the touch of your hand (Hey!)
    I want your leather-studded kiss in the sand
    I want your love
    Love, love, love, I want your love
    (Love, love, love, I want your love)
    
    [Pre-Chorus]
    You know that I want you
    And you know that I need you
    I want it bad
    Your bad romance
    
    [Chorus]
    I want your love, and I want your revenge
    You and me could write a bad romance (Oh-oh-oh-oh-oh)
    I want your love, and all your lover's revenge
    You and me could write a bad romance
    Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
    Caught in a bad romance
    Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
    Caught in a bad romance
    
    [Post-Chorus]
    Ra-ra-ah-ah-ah
    Roma-roma-ma
    Gaga, "Ooh la-la"
    Want your bad romance
    
    [Verse 2]
    I want your horror, I want your design
    ‘Cause you’re a criminal as long as you’re mine
    I want your love
    Love, love, love, I want your love, uh
    I want your psycho, your vertigo shtick (Shtick, hey!)
    Want you in my rear window, baby, you're sick
    I want your love
    Love, love, love, I want your love
    (Love, love, love, I want your love)
    
    [Pre-Chorus]
    You know that I want you
    And you know that I need you (
    'Cause I'm a free bitch, baby
    )
    I want it bad
    Your bad romance
    
    [Chorus]
    I want your love, and I want your revenge
    You and me could write a bad romance (Oh-oh-oh-oh-oh)
    I want your love, and all your lover's revenge
    You and me could write a bad romance
    Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
    Caught in a bad romance
    Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
    Caught in a bad romance
    
    [Post-Chorus]
    Ra-ra-ah-ah-ah
    Roma-roma-ma
    Gaga, "Ooh la-la"
    Want your bad romance
    Ra-ra-ah-ah-ah
    Roma-roma-ma
    Gaga, "Ooh la-la"
    Want your bad romance
    
    [Bridge 1]
    Walk, walk, fashion, baby
    Work it, move that bitch crazy
    Walk, walk, fashion, baby
    Work it, move that bitch crazy
    Walk, walk, fashion, baby
    Work it, move that bitch crazy
    Walk, walk, passion, baby
    Work it, I'm a free bitch, baby
    
    [Bridge 2]
    I want your love, and I want your revenge
    I want your love, I don't wanna be friends
    Je veux ton amour et je veux ta revanche
    Je veux ton amour, I don't wanna be friends
    (Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh)
    (I want you back) No, I don't wanna be friends
    (Caught in a bad romance) I don't wanna be friends
    Want your bad romance
    (Caught in a bad romance) Want your bad romance
    
    [Chorus]
    I want your love, and I want your revenge
    You and me could write a bad romance (Oh-oh-oh-oh-oh)
    I want your love, and all your lover's revenge
    You and me could write a bad romance
    Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
    (Want your bad romance)
    Caught in a bad romance (Want your bad romance)
    Oh-oh-oh-oh-oh, oh-oh-oh-oh, oh-oh-oh
    (Want your bad romance)
    Caught in a bad romance
    
    [Post-Chorus]
    Ra-ra-ah-ah-ah
    Roma, Roma-ma
    Gaga, "Ooh la-la"
    Want your bad romance
    """
    return render_template('song.html', name="Song Title", lyrics=lyrics,
                           song_id=song_id)


@root.route('/plot/<song_id>')
def plot(song_id):
    return render_template('index.html', song_id=song_id)


@root.route('/plot/<song_id>/data')
def get_plot_csv(song_id):
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


@root.route('/plot/<song_id>/params')
def get_d3_plot_params(song_id):
    return jsonify({'words': all_lyrics})
