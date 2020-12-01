from slap_dj.app.init import start_django_lite

start_django_lite()

from services.billboard_reader import read_billboard_yearly


def generate_song_to_db():
    read_billboard_yearly()


GENERATING = False


def start_generating():
    if not GENERATING:
        generate_song_to_db()


if __name__ == '__main__':
    start_generating()
